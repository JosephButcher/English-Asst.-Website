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

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Replace with your HTML file


# Route to create a new account
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

# Route to load user cache
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


# Route to get a question batch
@app.route('/get_question_batch/<int:user_id>', methods=['GET'])
def get_question_batch(user_id):
    """
    Retrieve a batch of questions for the user:
    - 2 unseen questions (if available)
    - 8 attempted questions (if available)
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


# Route to ask questions
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


# Run the app
if __name__ == '__main__':
    app.run(debug=config.DEBUG)
