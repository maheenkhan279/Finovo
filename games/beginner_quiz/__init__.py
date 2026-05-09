from flask import Blueprint

beginner_bp = Blueprint('beginner_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.beginner_quiz import routes

