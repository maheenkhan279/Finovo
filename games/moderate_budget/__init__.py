from flask import Blueprint

moderate_bp = Blueprint('moderate_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.moderate_budget import routes

