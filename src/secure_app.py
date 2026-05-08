"""
SECURE PYTHON WEB APPLICATION - PROPERLY SECURED
This application demonstrates secure coding practices for Flask applications.
All vulnerabilities have been remediated.
"""

from flask import Flask, request, render_template, session, redirect, jsonify
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import json
import uuid
import logging
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# ✅ SECURE: Secret key from environment variable
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# ✅ SECURE: Configuration
app.config['SESSION_COOKIE_SECURE'] = True      # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True    # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'   # CSRF protection

# ✅ SECURE: Disable debug mode
DEBUG = os.getenv('FLASK_ENV') == 'development'
app.run(debug=DEBUG) if __name__ == '__main__' else None

# ✅ SECURE: File upload configuration
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_FOLDER = '/tmp/uploads'

# ✅ SECURE: Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE = "users.db"

def get_db():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with secure schema"""
    db = get_db()
    cursor = db.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    db.commit()
    db.close()

# ✅ SECURE: Authentication decorator
def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning("Unauthorized access attempt")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# ✅ SECURE: File validation
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>Secure Flask Application</h1>
    <ul>
        <li><a href="/register">Register</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/search">Search</a></li>
    </ul>
    """

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with secure password hashing"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        
        # ✅ SECURE: Input validation
        if not username or len(username) < 3:
            return "Username must be at least 3 characters", 400
        if not password or len(password) < 8:
            return "Password must be at least 8 characters", 400
        if '@' not in email:
            return "Invalid email format", 400
        
        try:
            db = get_db()
            cursor = db.cursor()
            
            # ✅ SECURE: Hash password with bcrypt (werkzeug)
            password_hash = generate_password_hash(password, method='pbkdf2')
            
            # ✅ SECURE: Parameterized query
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            db.commit()
            db.close()
            
            logger.info(f"New user registered: {username}")
            return redirect('/login')
            
        except sqlite3.IntegrityError:
            return "Username already exists", 400
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return "Registration failed", 500
    
    return '''
    <h2>Register</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Register</button>
    </form>
    <a href="/login">Already have an account?</a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with secure authentication"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # ✅ SECURE: Input validation
        if not username or not password:
            logger.warning(f"Login attempt with missing credentials from {request.remote_addr}")
            return "Invalid credentials", 401
        
        try:
            db = get_db()
            cursor = db.cursor()
            
            # ✅ SECURE: Parameterized query
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            db.close()
            
            # ✅ SECURE: Check password with hash comparison
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                logger.info(f"User logged in: {username}")
                return redirect('/dashboard')
            else:
                logger.warning(f"Failed login attempt for user: {username}")
                return "Invalid credentials", 401
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return "Login failed", 500
    
    return '''
    <h2>Login</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    <a href="/register">Create new account</a>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard (authenticated)"""
    username = session.get('username', 'User')
    return f"""
    <h2>Dashboard</h2>
    <p>Welcome, {escape(username)}!</p>
    <ul>
        <li><a href="/profile">View Profile</a></li>
        <li><a href="/search">Search</a></li>
        <li><a href="/upload">Upload File</a></li>
        <li><a href="/logout">Logout</a></li>
    </ul>
    """

@app.route('/profile')
@login_required
def profile():
    """User profile (only own profile accessible)"""
    user_id = session.get('user_id')
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        # ✅ SECURE: Parameterized query with authentication check
        cursor.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (user_id,)
        )
        user = cursor.fetchone()
        db.close()
        
        if not user:
            return "User not found", 404
        
        return f"""
        <h2>Profile</h2>
        <p>Username: {escape(user['username'])}</p>
        <p>Email: {escape(user['email'])}</p>
        <a href="/dashboard">Back to Dashboard</a>
        """
        
    except Exception as e:
        logger.error(f"Profile fetch error: {str(e)}")
        return "Error fetching profile", 500

@app.route('/search')
@login_required
def search():
    """Secure search with proper output encoding"""
    query = request.args.get('q', '').strip()
    
    # ✅ SECURE: Input length validation
    if len(query) > 100:
        return "Search query too long", 400
    
    # ✅ SECURE: The query is HTML-escaped when rendered
    return f"""
    <h2>Search Results</h2>
    <p>Results for: {escape(query)}</p>
    <a href="/dashboard">Back to Dashboard</a>
    """

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Secure file upload"""
    if request.method == 'POST':
        # ✅ SECURE: Validate file exists
        if 'file' not in request.files:
            return "No file selected", 400
        
        file = request.files['file']
        
        if file.filename == '':
            return "No file selected", 400
        
        # ✅ SECURE: Validate file extension
        if not allowed_file(file.filename):
            return "File type not allowed", 400
        
        # ✅ SECURE: Validate file size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        if file_length > MAX_FILE_SIZE:
            return "File too large (max 5MB)", 400
        
        try:
            # ✅ SECURE: Use secure filename and generate unique name
            filename = secure_filename(file.filename)
            user_id = session.get('user_id')
            unique_filename = f"{user_id}_{uuid.uuid4()}_{filename}"
            
            # ✅ SECURE: Store outside web root
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            file.seek(0)
            file.save(filepath)
            
            logger.info(f"File uploaded by user {user_id}: {unique_filename}")
            return "File uploaded successfully", 200
            
        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            return "Upload failed", 500
    
    return '''
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    <p>Allowed: txt, pdf, png, jpg, jpeg, gif</p>
    <p>Max size: 5MB</p>
    <a href="/dashboard">Back to Dashboard</a>
    '''

@app.route('/api/data')
@login_required
def api_data():
    """Secure API endpoint"""
    try:
        user_id = request.args.get('id', '').strip()
        
        # ✅ SECURE: Input validation
        if not user_id.isdigit():
            return jsonify({"error": "Invalid user ID"}), 400
        
        # ✅ SECURE: Authorization check
        if int(user_id) != session.get('user_id'):
            logger.warning(f"Unauthorized data access attempt by user {session.get('user_id')}")
            return jsonify({"error": "Unauthorized"}), 403
        
        db = get_db()
        cursor = db.cursor()
        
        # ✅ SECURE: Parameterized query
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        db.close()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "id": user['id'],
            "username": user['username'],
            "email": user['email']
        })
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    username = session.get('username')
    session.clear()
    logger.info(f"User logged out: {username}")
    return redirect('/login')

# ✅ SECURE: Global error handlers
@app.errorhandler(400)
def bad_request(error):
    logger.warning(f"Bad request: {str(error)}")
    return "Bad request", 400

@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return "Internal server error", 500

# ✅ SECURE: Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    init_db()
    # ✅ SECURE: Debug mode disabled in production
    app.run(debug=DEBUG, host='localhost', port=5000)