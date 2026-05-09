from flask import Blueprint

moderate_loan_bp = Blueprint('moderate_loan_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.moderate_loan_game import routes

