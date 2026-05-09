from flask import Blueprint

advanced_bp = Blueprint('advanced_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.advanced_stock import routes

