from flask import request, jsonify, render_template
import random
import bcrypt
from datetime import datetime
from backend import create_app
from backend.config import config

# Initialize Flask app
app = create_app()

# Database connection and cursor
connection = config.DB_CONNECTION_STRING
cursor = connection.cursor()

user_cache = {}

#################################################################################### Route for the home page ##############################################################################
@app.route('/')
def home():
    return render_template('index.html')  # Replace with your HTML file


################################################################################## Route to create a new account #####################################################################################
@app.route('/create_account', methods=['POST'])
def create_account():
    # Ensure the 'users' table exists
    table_check_query = """
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'users'
    )
    BEGIN
        CREATE TABLE dbo.users (
            user_id INT IDENTITY(1,1) PRIMARY KEY,
            username VARCHAR(30) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE
        )
    END;
    """
    cursor.execute(table_check_query)
    connection.commit()

    # Get user details from the request
    data = request.json
    username = data.get('username')
    user_email = data.get('email')
    user_pass = data.get('password')


    # Validate inputs
    if not username or not user_email or not user_pass:
        return jsonify({'error': 'All fields (username, password, email) are required'}), 400
    if len(user_pass) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    if '@' not in user_email or '.' not in user_email:  # Basic email validation
        return jsonify({'error': 'Invalid email format'}), 400

    # Check if username or email already exists
    check_user_query = """
    SELECT COUNT(*) FROM users WHERE username = ? OR email = ?
    """
    cursor.execute(check_user_query, (username, user_email))
    user_exists = cursor.fetchone()[0]
    if user_exists:
        return jsonify({'error': 'Username or email already exists'}), 409

    # Hash the password
    hashed_password = bcrypt.hashpw(user_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert user into the database
    try:
        sql_query = """INSERT INTO users(username, password, email) VALUES (?, ?, ?)"""
        cursor.execute(sql_query, (username, hashed_password, user_email))
        connection.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

################################################################################## Route to login to account #####################################################################################

@app.route('/login_account', methods=['POST'])
def login_account():
    # Get login details from the request
    data = request.json
    username = data.get('username')
    user_pass = data.get('password')

    # Validate inputs
    if not username or not user_pass:
        return jsonify({'error': 'Both username and password are required'}), 400

    try:
        # Query to fetch the user's data (password) from the database
        cursor.execute('SELECT username, password FROM dbo.users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Incorrect username. Try again or create an account.'}), 404

        # Verify the password
        stored_password = user[1]
        if bcrypt.checkpw(user_pass.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'error': 'Incorrect password'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

################################################################################## Route to getting word for definitions page (not sure how these will return in vue if they don't work lmk and I'll come over!!) #####################################################################################


@app.route('/start_new_word', methods=['GET'])
def start_new_word():
    """
    Fetches a random word and its questions, starting the quiz for a new user.
    """
    try:
        # Fetch a random word from the dbo.words table
        cursor.execute('SELECT word_id, word, definition, part_of_speech, synonyms, example_sentence FROM dbo.words ORDER BY NEWID() LIMIT 1')
        word_row = cursor.fetchone()

        if not word_row:
            return jsonify({'error': 'No words found in the database.'}), 404

        word_id, word, definition, part_of_speech, synonyms, example_sentence = word_row

        # Fetch questions related to this word
        cursor.execute('SELECT question_id, text, correct_answer FROM dbo.questions WHERE word_id = ?', (word_id,))
        questions = [
            {
                'question_id': row[0],
                'text': row[1],
                'correct_answer': row[2]
            }
            for row in cursor.fetchall()
        ]

        # Initialize user progress (e.g., step 1 = spelling check)
        user_progress = {
            'current_step': 2,  # Start at the spelling check
            'word_id': word_id,
            'questions': questions
        }

        # Respond with word data and initial user progress
        response = {
            'word': word,
            'definition': definition,
            'part_of_speech': part_of_speech,
            'synonyms': synonyms,
            'example_sentence': example_sentence,
            'questions': questions,
            'user_progress': user_progress
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch word data: {str(e)}'}), 500


################################################################################## Route to check the answers (same with these!) #####################################################################################



@app.route('/update_user_progress', methods=['POST'])
def update_user_progress():
    """
    Update user's progress based on their answer.
    """
    data = request.json
    user_id = data.get('user_id')
    word_id = data.get('word_id')
    correct_answer = data.get('correct_answer')
    user_answer = data.get('user_answer')

    # Check if the user's answer is correct
    is_correct = correct_answer.lower() == user_answer.lower()

    # Track user progress in the database
    try:
        cursor = connection.cursor()
        
        if is_correct:
            cursor.execute('UPDATE dbo.user_progress SET current_step = current_step + 1 WHERE user_id = ? AND word_id = ?', (user_id, word_id))
        else:
            cursor.execute('UPDATE dbo.user_progress SET current_step = 2 WHERE user_id = ? AND word_id = ?', (user_id, word_id))  # Reset to spelling check if wrong

        connection.commit()

        return jsonify({'status': 'success', 'is_correct': is_correct}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500


################################################################################## Route to load user cache (everything here and beyond isn't necessary rn. Only the stuff above is what we need to get done!) #####################################################################################
@app.route('/load_user_cache/<int:user_id>', methods=['GET'])
def load_user_cache(user_id):
    """
    Load the user's cache with unseen and attempted questions.
    """
    unseen_query = """
        SELECT q.question_id
        FROM questions q
        LEFT JOIN user_progress up ON q.question_id = up.question_id AND up.user_id = ?
        WHERE up.question_id IS NULL;
    """
    attempted_query = """
        SELECT question_id, attempt_count, accurate_count, last_attempted
        FROM user_progress
        WHERE user_id = ?;
    """

    try:
        # Fetch unseen questions
        cursor.execute(unseen_query, user_id)
        unseen_questions = {row[0]: None for row in cursor.fetchall()}

        # Fetch attempted questions
        cursor.execute(attempted_query, user_id)
        attempted_questions = {
            row[0]: {
                "attempt_count": row[1],
                "accurate_count": row[2],
                "last_attempted": row[3].isoformat() if row[3] else None
            }
            for row in cursor.fetchall()
        }

        # Update user cache
        user_cache[user_id] = {
            "unseen_questions": unseen_questions,
            "attempted_questions": attempted_questions,
            "last_updated": datetime.now().isoformat()
        }

        return jsonify(user_cache[user_id]), 200
    except Exception as e:
        return jsonify({'error': f'Failed to load user cache: {str(e)}'}), 500


################################################################################## Route to create a question batch #####################################################################################
@app.route('/get_question_batch/<int:user_id>', methods=['GET'])
def get_question_batch(user_id):
    """
    Retrieve a batch of questions for the user:
    - 5 unseen questions (if available)
    - 5 attempted questions (if available)
    - Random questions to fill the batch if needed
    """
    if user_id not in user_cache:
        return jsonify({'error': 'User cache not loaded. Please load it first.'}), 400

    try:
        batch = []

        # Add unseen questions
        unseen_questions = user_cache[user_id]["unseen_questions"]
        for _ in range(5):
            if unseen_questions:
                question_id, _ = unseen_questions.popitem()
                batch.append(question_id)

        # Add attempted questions
        attempted_questions = user_cache[user_id]["attempted_questions"]
        for _ in range(5 - len(batch)):
            if attempted_questions:
                question_id, _ = attempted_questions.popitem()
                batch.append(question_id)

        # Add random questions to complete the batch
        while len(batch) < 10:
            random_id = random.randint(0, 612)
            if random_id not in batch:
                batch.append(random_id)

        return jsonify({'batch': batch}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve question batch: {str(e)}'}), 500


################################################################################## Route to ask questions #####################################################################################
@app.route('/ask_questions', methods=['POST'])
def ask_questions():
    """
    Retrieve details for a list of question IDs provided by the user.
    """
    data = request.json
    user_id = data.get('user_id')
    question_ids = data.get('questions', [])

    # Validate input
    if not user_id or not isinstance(question_ids, list) or not question_ids:
        return jsonify({'error': 'Invalid input. Provide user_id and a list of question IDs.'}), 400

    try:
        questions = []

        # Fetch question details
        query = "SELECT question_id, text, correct_answer FROM questions WHERE question_id = ?"
        for question_id in question_ids:
            cursor.execute(query, question_id)
            question = cursor.fetchone()
            if question:
                questions.append({
                    'id': question[0],
                    'text': question[1],
                    'correct_answer': question[2]
                })

        return jsonify({'questions': questions}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch questions: {str(e)}'}), 500

################################################################################## Route to track answers #####################################################################################
@app.route('/track_attempt', methods=['POST'])
def track_attempt():
    """
    This route receives a user ID, question, and answer, checks if the answer is correct,
    and updates the user progress in the database.
    """
    data = request.json
    user_id = data.get('user_id')
    question = data.get('question')  # Expected to be a dictionary containing the question data
    answer = data.get('answer')

    # Check if the necessary fields are provided
    if not user_id or not question or not answer:
        return jsonify({'error': 'User ID, question, and answer are required'}), 400

    # Check if the question data is in the expected format
    if 'question_id' not in question or 'type' not in question or 'correct_answer' not in question:
        return jsonify({'error': 'Invalid question format'}), 400

    try:
        # Determine if the answer is correct
        is_correct = (
            (question['type'] == "multiple_choice" and answer.lower() == question['correct_answer'][0].lower()) or
            question['correct_answer'].lower() == answer.lower()
        )

        # Determine outcome (1 for correct, 0 for incorrect)
        outcome = 1 if is_correct else 0
        question_id = question['question_id']

        # Perform database operations
        cursor = connection.cursor()

        # Insert into user progress table (if not already present)
        cursor.execute(
            '''
            INSERT INTO dbo.user_progress (user_id, question_id)
            VALUES (?, ?)
            ''',
            user_id, question_id
        )

        # Update the user progress table based on the outcome
        if outcome == 1:
            cursor.execute(
                '''
                UPDATE dbo.user_progress
                SET accurate_count = accurate_count + 1,
                    attempt_count = attempt_count + 1
                WHERE user_id = ? AND question_id = ?;
                ''',
                user_id, question_id
            )
        else:
            cursor.execute(
                '''
                UPDATE dbo.user_progress
                SET attempt_count = attempt_count + 1
                WHERE user_id = ? AND question_id = ?;
                ''',
                user_id, question_id
            )

        connection.commit()

        # Return success response to the client
        return jsonify({'message': 'Attempt recorded successfully', 'outcome': outcome, 'question_id': question_id}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()




# Run the app
if __name__ == '__main__':
    app.run(debug=config.DEBUG)
