from flask import Blueprint

beginner_savings_challenge_bp = Blueprint('beginner_savings_challenge_bp', __name__)

from games.beginner_savings_challenge import routes  # noqa: E402, F401
