# FINOVO Authentication System

## Overview

A clean, beginner-friendly authentication system has been implemented for the FINOVO platform. Users must register and login to access the financial learning games.

## Features

✅ **User Registration** - Create new accounts with username, email, and password
✅ **User Login** - Secure login with password hashing
✅ **Session Management** - Persistent sessions during gameplay
✅ **Protected Routes** - All games require authentication
✅ **Clean UI** - Professional login/register pages matching FINOVO theme
✅ **Navigation Updates** - Dynamic login/logout buttons based on auth status

## Database

- **Database**: SQLite (`finovo.db`)
- **User Model**: 
  - `id` (Primary Key)
  - `username` (Unique, Indexed)
  - `email` (Unique, Indexed)
  - `password_hash` (Hashed with Werkzeug)

## Routes

### Public Routes
- `/` - Homepage (no login required)
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout

### Protected Routes (Require Login)
- `/games` - Games listing page
- `/games/beginner` - Beginner game
- `/games/moderate` - Moderate game
- `/games/advanced` - Advanced game

## Files Created/Modified

### New Files
1. **`models.py`** - User model with password hashing
2. **`auth.py`** - Authentication utilities (login_required decorator)
3. **`templates/login.html`** - Login page
4. **`templates/register.html`** - Registration page

### Modified Files
1. **`app.py`** - Added database setup, auth routes, and user loading
2. **`templates/base.html`** - Updated navigation to show login/logout
3. **`games/beginner_quiz/routes.py`** - Added @login_required decorator
4. **`games/moderate_budget/routes.py`** - Added @login_required decorator
5. **`games/advanced_stock/routes.py`** - Added @login_required decorator
6. **`requirements.txt`** - Added Flask-SQLAlchemy

## Security Features

- **Password Hashing**: Uses Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session Management**: Secure session handling with Flask sessions
- **Input Validation**: Username, email, and password validation
- **Duplicate Prevention**: Checks for existing usernames and emails
- **Password Requirements**: Minimum 6 characters

## Usage

### For Users

1. **Register**: Click "Sign Up" → Fill form → Create account
2. **Login**: Click "Login" → Enter credentials → Access games
3. **Play Games**: All games are now accessible after login
4. **Logout**: Click "Logout" to end session

### For Developers

The `@login_required` decorator can be added to any route:

```python
from auth import login_required

@app.route('/protected')
@login_required
def protected_route():
    return "This requires login"
```

## Database Initialization

The database is automatically created on first run. The `finovo.db` file will be created in the project root directory.

## Testing

1. Start the application: `python app.py`
2. Navigate to `/register` and create an account
3. Login at `/login`
4. Try accessing `/games` - should work
5. Logout and try accessing `/games` - should redirect to login
6. Login again - should redirect back to games

## Notes

- No virtual environment required
- Database file (`finovo.db`) is created automatically
- Sessions persist during gameplay
- All game routes are protected
- Homepage remains public for marketing purposes

