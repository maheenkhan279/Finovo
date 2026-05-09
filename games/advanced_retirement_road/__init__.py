from flask import Blueprint

advanced_retirement_road_bp = Blueprint('advanced_retirement_road_bp', __name__)

from games.advanced_retirement_road import routes  # noqa: E402, F401
