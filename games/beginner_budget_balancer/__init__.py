from flask import Blueprint

beginner_budget_bp = Blueprint('beginner_budget_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.beginner_budget_balancer import routes

