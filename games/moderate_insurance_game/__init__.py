from flask import Blueprint

moderate_insurance_bp = Blueprint('moderate_insurance_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.moderate_insurance_game import routes

