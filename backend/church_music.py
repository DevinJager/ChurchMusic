"""
Church Music Repository Flask
"""

from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'secret_key'  # Need to figure out what secret key to use
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Function to get a database connection
# def get_db():
#     db = sqlite3.connect('Church_Music_Repository.db')
#     db.row_factory = sqlite3.Row  # Return rows as dictionaries
#     return db

def get_db():
    try:
        db = sqlite3.connect('Church_Music_Repository.db')
        db.row_factory = sqlite3.Row  # Return rows as dictionaries
        print("Database connected successfully")
        return db
    except Exception as e:
        print(f"Database connection failed: {e}")

# User class, using user, email or password
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    @staticmethod
    def get_by_username(email):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password FROM user WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return User(*row) if row else None

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Signup, used to initially create the admin profile in order to use the correct hashing for password
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            db = get_db()
            cursor = db.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM user WHERE email = ?", (email,))
            if cursor.fetchone():
                flash('Email already registered!', 'danger')
                return redirect(url_for('signup'))

            # Insert new user
            cursor.execute("INSERT INTO user (email, password) VALUES (?, ?)", (email, hashed_password))
            db.commit()

            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')

    return render_template('signup.html')  

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.get_by_username(email)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful", "user": {"email": user.email}}), 200
    else:
        pass
        #return jsonify({"error": "Invalid email or password"}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/user', methods=['GET'])
def get_user():
    if current_user.is_authenticated:
        return jsonify({"email": current_user.email}), 200
    return jsonify({"error": "Not authenticated"}), 401

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.get_by_username(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('musiclibrary'))
        else:
            pass
            #flash('Invalid email or password', 'danger')

    return render_template('login.html')  

@app.route('/index/<table_name>')
@login_required
def index(table_name):
    try:
        db = get_db()
        cursor = db.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            flash(f"Table '{table_name}' not found.", "danger")
            return redirect(url_for('musiclibrary'))

        # Fetch data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        # Convert to a list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]
        db.close()

        return render_template('index.html', data=data, table_name=table_name)

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('musiclibrary'))

# User logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
'''
@app.route('/data/<table_name>', methods=['GET'])
def get_data_report(table_name):
    try:
        db = get_db()
        cursor = db.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return jsonify({"error": f"Table '{table_name}' not found"}), 404

        # Get filters as comma-separated strings from query params
        filter_columns = request.args.get('filter_columns')
        filter_values = request.args.get('filter_values')

        query = f"SELECT * FROM {table_name}"
        params = []

        # Process multiple filters if provided
        if filter_columns and filter_values:
            filter_columns = filter_columns.split(',')
            filter_values = filter_values.split(',')

            if len(filter_columns) != len(filter_values):
                return jsonify({"error": "Mismatched number of columns and values"}), 400

            conditions = [f"{col.strip()} = ?" for col in filter_columns]
            query += " WHERE " + " AND ".join(conditions)
            params.extend([val.strip() for val in filter_values])

        # Execute query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        # Convert rows to JSON
        data = [dict(zip(columns, row)) for row in rows]
        db.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
@app.route('/data/<table_name>', methods=['GET'])
def get_data(table_name):
    try:
        db = get_db()
        cursor = db.cursor()

        # Validate table existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return jsonify({"error": f"Table '{table_name}' not found"}), 404
        
        # Apply filtering if provided
        filter_column = request.args.get('filter_column')
        filter_value = request.args.get('filter_value')

        query = f"SELECT * FROM {table_name}"
        params = []

        if filter_column and filter_value:
            query += f" WHERE {filter_column} = ?"
            params.append(filter_value)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        # Convert to JSON
        data = [dict(zip(columns, row)) for row in rows]
        db.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/data/<table_name>', methods=['POST'])
def add_data(table_name):
    try:
        db = get_db()
        cursor = db.cursor()

        # Get JSON data from request
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Dynamically create query based on keys
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Entry added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update or edit existing 
@app.route('/data/<table_name>/<int:entry_id>', methods=['PUT'])
def update_data(table_name, entry_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        updates = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (entry_id,)

        query = f"UPDATE {table_name} SET {updates} WHERE id = ?"
        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Entry updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete from the database 
@app.route('/data/<table_name>/<int:entry_id>', methods=['DELETE'])
def delete_data(table_name, entry_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entry_id,))
        db.commit()

        return jsonify({"message": "Entry deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run Flask app on port 5001
if __name__ == '__main__':
    app.run(port=5001, debug=True)