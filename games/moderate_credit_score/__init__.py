from flask import Blueprint

moderate_credit_score_bp = Blueprint('moderate_credit_score_bp', __name__)

from games.moderate_credit_score import routes  # noqa: E402, F401
