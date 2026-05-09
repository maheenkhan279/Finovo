from flask import Blueprint

advanced_portfolio_bp = Blueprint('advanced_portfolio_bp', __name__)

# Import routes after blueprint creation to avoid circular imports
from games.advanced_portfolio_tool import routes

