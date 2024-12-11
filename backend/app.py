from flask import Flask, request, jsonify, render_template
import random
import bcrypt
from datetime import datetime
import pyodbc  # Ensure this import is at the top
from flask_cors import CORS  # Import once

# Configuration for DB connection and other settings (ensure the config file exists)
from backend.config import config

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow CORS for all routes

# Database connection and cursor
connection = pyodbc.connect(config.DB_CONNECTION_STRING)  # Use pyodbc to connect to the database
cursor = connection.cursor()  # Create cursor from the connection

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
        if bcrypt.checkpw(user_pass.encode('utf-8'), stored_password.encode('utf-8')):  # Compare hash
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'error': 'Incorrect password'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


################################################################################## Route to getting word for definitions page #####################################################################################

@app.route('/start_new_word', methods=['GET'])
def start_new_word():
    """
    Fetches a random word and its questions, starting the quiz for a new user.
    """
    try:
        # Fetch a random word from the dbo.words table
        cursor.execute(
            'SELECT word_id, word, definition, part_of_speech, synonyms, example_sentence FROM dbo.words ORDER BY NEWID()')
        word_row = cursor.fetchone()

        if not word_row:
            return jsonify({'error': 'No words found in the database.'}), 404

        word_id, word, definition, part_of_speech, synonyms, example_sentence = word_row

        response = {
            'word': word,
            'definition': definition,
            'part_of_speech': part_of_speech,
            'example_sentence': example_sentence,
            'synonyms': synonyms,
            'spelling': word
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch word data: {str(e)}'}), 500


################################################################################## Route to check the answers #####################################################################################

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
            cursor.execute(
                'UPDATE dbo.user_progress SET current_step = current_step + 1 WHERE user_id = ? AND word_id = ?',
                (user_id, word_id))
        else:
            cursor.execute('UPDATE dbo.user_progress SET current_step = 2 WHERE user_id = ? AND word_id = ?',
                           (user_id, word_id))  # Reset to spelling check if wrong

        connection.commit()

        return jsonify({'status': 'success', 'is_correct': is_correct}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to update progress: {str(e)}'}), 500


@app.route('/check_spelling', methods=['POST'])
def check_spelling():
    data = request.get_json()

    print("Received data:", data)  # Debugging line to print received data

    word = data.get('word', '').strip().lower()  # User input
    correct_word = data.get('correct_word', '').strip().lower()  # The correct word to compare

    # Check if both 'word' and 'correct_word' are provided
    if word and correct_word:
        if word == correct_word:
            return jsonify({"success": True, "message": "Spelling is correct!"})
        else:
            return jsonify({"success": False, "message": "Incorrect spelling."})
    else:
        return jsonify({"success": False, "message": "Invalid input, word or correct_word missing."})









# Run the app
if __name__ == '__main__':
    app.run(debug=True)
