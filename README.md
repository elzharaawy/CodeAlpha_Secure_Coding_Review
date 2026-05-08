# Secure Coding Review - Python Flask Application

## 📋 Overview

This project demonstrates a complete **security code review** of a Python Flask web application. It includes:

- **Vulnerable Application** - Flask app with 9 critical security vulnerabilities
- **Security Audit Report** - Detailed analysis of all security issues
- **Secure Application** - Fixed version with all vulnerabilities remediated
- **Remediation Guide** - Step-by-step instructions to fix security issues
- **Best Practices** - Guidelines for secure coding in Python/Flask

## 🎯 Project Goal

Learn common web application security vulnerabilities and how to fix them:

✗ **Before**: Vulnerable code with security flaws
✓ **After**: Secure code following best practices

## 🔴 Vulnerabilities Found

| #   | Vulnerability              | Severity | Type          |
| --- | -------------------------- | -------- | ------------- |
| 1   | SQL Injection (3x)         | CRITICAL | Database      |
| 2   | Hardcoded Secret Key       | CRITICAL | Configuration |
| 3   | Cross-Site Scripting (XSS) | CRITICAL | Input         |
| 4   | Missing Authentication     | CRITICAL | Authorization |
| 5   | Unsafe File Upload         | CRITICAL | File Handling |
| 6   | Unsafe Deserialization     | CRITICAL | Serialization |
| 7   | Debug Mode Enabled         | HIGH     | Configuration |
| 8   | Information Disclosure     | HIGH     | Output        |
| 9   | API SQL Injection          | CRITICAL | Database      |

**Status**: All 9 vulnerabilities identified and fixed ✓

## 📁 Project Structure

```
secure-coding-review/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── .env.example                       # Environment variables template
│
├── docs/                              # Documentation
│   ├── SECURITY_REVIEW_REPORT.txt    # Detailed vulnerability analysis
│   ├── REMEDIATION_GUIDE.txt         # Step-by-step fix instructions
│   ├── TASK_COMPLETION_SUMMARY.txt   # Project summary
│   └── BEST_PRACTICES.md             # Coding best practices
│
├── src/                               # Source code
│   ├── vulnerable_app.py             # Before: 9 vulnerabilities
│   └── secure_app.py                 # After: All fixed
│
├── tests/                             # Security tests
│   ├── test_auth.py                  # Authentication tests
│   ├── test_security.py              # Security vulnerability tests
│   └── test_validation.py            # Input validation tests
│
└── config/                            # Configuration modules
    ├── development.py                # Development settings
    ├── production.py                 # Production settings
    └── testing.py                    # Testing settings
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/secure-coding-review.git
cd secure-coding-review
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
cp .env.example .env
# Edit .env and add your SECRET_KEY
# Generate key: python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run Secure Application

```bash
python src/secure_app.py
```

Visit: `http://localhost:5000`

### 5. Run Tests

```bash
pytest tests/
```

## 📚 Documentation

### Main Reports

- **[SECURITY_REVIEW_REPORT.txt](docs/SECURITY_REVIEW_REPORT.txt)** (3,200+ lines)
  - Comprehensive analysis of all 9 vulnerabilities
  - Code samples (vulnerable vs secure)
  - Impact assessment
  - Remediation steps

- **[REMEDIATION_GUIDE.txt](docs/REMEDIATION_GUIDE.txt)** (2,500+ lines)
  - 12 step-by-step implementation guides
  - Side-by-side code comparisons
  - Testing procedures
  - Deployment checklist

- **[TASK_COMPLETION_SUMMARY.txt](docs/TASK_COMPLETION_SUMMARY.txt)**
  - Project overview
  - Vulnerabilities summary
  - Best practices
  - Next steps

### Code Files

- **[vulnerable_app.py](src/vulnerable_app.py)** - Intentionally vulnerable for learning
- **[secure_app.py](src/secure_app.py)** - Production-ready secure version

## 🔍 Vulnerability Details

### SQL Injection (3 instances)

```python
# ❌ VULNERABLE
cursor.execute(f"SELECT * FROM users WHERE username='{username}'")

# ✅ SECURE
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
```

### Hardcoded Secrets

```python
# ❌ VULNERABLE
app.secret_key = "hardcoded_secret_key_12345"

# ✅ SECURE
app.secret_key = os.getenv('SECRET_KEY')
```

### Cross-Site Scripting (XSS)

```python
# ❌ VULNERABLE
return f"<h1>Results for: {query}</h1>"

# ✅ SECURE
return f"<h1>Results for: {escape(query)}</h1>"
```

### Missing Authentication

```python
# ❌ VULNERABLE
@app.route('/profile/<user_id>')
def profile(user_id):
    # No authentication check!

# ✅ SECURE
@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    # Check user can only access their own data
    if int(user_id) != session.get('user_id'):
        return "Unauthorized", 403
```

See [SECURITY_REVIEW_REPORT.txt](docs/SECURITY_REVIEW_REPORT.txt) for all vulnerabilities.

## 🛠️ Security Features in Secure Version

✅ Parameterized database queries
✅ Environment-based secrets
✅ HTML output escaping (XSS prevention)
✅ Authentication & authorization
✅ Secure file upload handling
✅ Safe JSON deserialization
✅ Debug mode disabled in production
✅ Security headers (CSP, HSTS, X-Frame-Options)
✅ Password hashing (pbkdf2)
✅ Comprehensive logging
✅ Input validation
✅ Error handling

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Specific Module

```bash
pytest tests/test_security.py -v
```

### Generate Coverage Report

```bash
pytest --cov=src tests/
```

### Security Tools

```bash
# Check for vulnerabilities in code
bandit -r src/

# Check for vulnerable dependencies
safety check

# Python package audit
pip-audit
```

## 📋 Best Practices Implemented

### 1. Input Validation

- Server-side validation on all inputs
- Whitelist approach for file extensions
- Type checking and length limits

### 2. Database Security

- Parameterized queries (prepared statements)
- Principle of least privilege
- No database error exposure to users

### 3. Authentication

- Secure password hashing (pbkdf2)
- Session-based authentication
- Authorization checks on protected routes

### 4. Secrets Management

- No hardcoded secrets
- Environment variables for configuration
- .env file excluded from version control

### 5. Output Encoding

- HTML escaping in responses
- Jinja2 templates for safe rendering
- JSON encoding for APIs

### 6. Error Handling

- Generic error messages to users
- Detailed logging for debugging
- No stack trace exposure in production

### 7. Security Headers

- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security
- Content-Security-Policy

## 🔐 Production Checklist

Before deploying to production:

- [ ] All vulnerabilities fixed
- [ ] Security tests passing
- [ ] Debug mode disabled
- [ ] .env configured with production values
- [ ] HTTPS/TLS enabled
- [ ] Security headers verified
- [ ] Dependencies updated
- [ ] Logging and monitoring configured
- [ ] Penetration testing completed
- [ ] Code review by security professional

## 📦 Dependencies

- Flask==3.0.0 - Web framework
- Werkzeug==3.0.0 - WSGI utilities & password hashing
- python-dotenv==1.0.0 - Environment variable management
- pytest==7.0.0 - Testing framework (optional)

See [requirements.txt](requirements.txt) for full list.

## 🔄 How to Compare

### View Differences

```bash
diff src/vulnerable_app.py src/secure_app.py
```

### Run Both Versions (in different terminals)

```bash
# Terminal 1: Vulnerable version
python src/vulnerable_app.py

# Terminal 2: Secure version
python src/secure_app.py
```

## 📖 Learning Path

1. **Start Here**: Read [TASK_COMPLETION_SUMMARY.txt](docs/TASK_COMPLETION_SUMMARY.txt)
2. **Study Issues**: Review [SECURITY_REVIEW_REPORT.txt](docs/SECURITY_REVIEW_REPORT.txt)
3. **Learn Fixes**: Follow [REMEDIATION_GUIDE.txt](docs/REMEDIATION_GUIDE.txt)
4. **Compare Code**: Study [vulnerable_app.py](src/vulnerable_app.py) vs [secure_app.py](src/secure_app.py)
5. **Run Tests**: Execute security tests in [tests/](tests/)
6. **Practice**: Implement fixes in your own projects

## 🎓 Key Takeaways

### What You'll Learn

✓ Common web application vulnerabilities
✓ How to identify security issues
✓ How to fix security vulnerabilities
✓ Best practices for secure coding
✓ How to use security tools
✓ Testing for security issues
✓ Secure development workflow

### Real-World Application

These vulnerabilities are found in real applications:

- 60% of web apps have SQL injection vulnerabilities
- 40% have XSS vulnerabilities
- 30% have authentication issues

This project helps you understand and prevent them!

## 🔗 Resources

### Security Standards

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Security Cheat Sheet](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

### Python Security

- [Flask Security](https://flask.palletsprojects.com/security/)
- [Python Security](https://python.readthedocs.io/security/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)

### Testing Tools

- [bandit](https://bandit.readthedocs.io/) - Security linter
- [safety](https://safety.readthedocs.io/) - Dependency checker
- [pip-audit](https://github.com/pypa/pip-audit) - Package auditor

### Web Security

- [Burp Suite](https://portswigger.net/burp) - Security testing
- [OWASP ZAP](https://www.zaproxy.org/) - Web scanner

## 💡 Contributing

If you find issues or have improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes.

## 🙋 Questions?

Refer to:

- [SECURITY_REVIEW_REPORT.txt](docs/SECURITY_REVIEW_REPORT.txt) - Technical details
- [REMEDIATION_GUIDE.txt](docs/REMEDIATION_GUIDE.txt) - How-to instructions
- [BEST_PRACTICES.md](docs/BEST_PRACTICES.md) - Quick reference

## ✅ Completion Status

- [x] Vulnerable application created
- [x] Security audit completed
- [x] 9 vulnerabilities identified
- [x] Secure version developed
- [x] Remediation guide written
- [x] Tests created
- [x] Documentation completed
- [x] Ready for GitHub

## 📅 Created

**May 8, 2026** - Task 1: Secure Coding Review

---

**Made with ❤️ for learning secure coding practices**
