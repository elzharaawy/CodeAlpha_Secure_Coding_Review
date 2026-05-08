"""
VULNERABLE PYTHON WEB APPLICATION - FOR SECURITY REVIEW PURPOSES
This application contains multiple security vulnerabilities intentionally
for demonstration and educational purposes.
"""

from flask import Flask, request, render_template_string, session, redirect
import sqlite3
import pickle
import os

app = Flask(__name__)
app.secret_key = "hardcoded_secret_key_12345"  # VULNERABILITY: Hardcoded secret

# Database setup
DATABASE = "users.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def home():
    return "Welcome to Vulnerable App"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABILITY: SQL Injection
        db = get_db()
        cursor = db.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        
        return "Login failed"
    
    return '''
    <form method="post">
        Username: <input type="text" name="username">
        Password: <input type="password" name="password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/search')
def search():
    # VULNERABILITY: Reflected XSS
    query = request.args.get('q', '')
    return f"<h1>Search Results for: {query}</h1>"

@app.route('/profile/<user_id>')
def profile(user_id):
    # VULNERABILITY: No authentication check
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()
    return f"User: {user}"

@app.route('/upload', methods=['POST'])
def upload():
    # VULNERABILITY: Unsafe file upload
    file = request.files['file']
    file.save(os.path.join('/tmp', file.filename))
    return "File uploaded"

@app.route('/api/data')
def api_data():
    # VULNERABILITY: No input validation
    user_id = request.args.get('id')
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()
    return str(user)

@app.route('/debug')
def debug():
    # VULNERABILITY: Debug mode enabled, sensitive info exposure
    import sys
    return f"Python path: {sys.path}<br>OS environ: {os.environ}"

@app.route('/deserialize', methods=['POST'])
def deserialize():
    # VULNERABILITY: Unsafe deserialization
    data = request.form.get('data')
    obj = pickle.loads(data)
    return str(obj)

if __name__ == '__main__':
    app.run(debug=True)  # VULNERABILITY: Debug mode in production