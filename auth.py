from functools import wraps
from flask import session, redirect, url_for, g
from models import User, db

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            from flask import request
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def load_logged_in_user():
    """Load user from session into g.user"""
    user_id = session.get('user_id')
    print(f"DEBUG: load_logged_in_user - session user_id: {user_id}")
    if user_id is None:
        g.user = None
        print("DEBUG: No user_id in session, g.user set to None")
    else:
        g.user = User.query.get(user_id)
        print(f"DEBUG: User loaded from database: {g.user is not None}")
        if g.user:
            print(f"DEBUG: Loaded user - ID: {g.user.id}, Username: {g.user.username}")
        else:
            print("DEBUG: User not found in database for user_id")

