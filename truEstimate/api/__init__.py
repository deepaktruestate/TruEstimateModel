# truEstimate/api/__init__.py

from flask import Blueprint

property_bp = Blueprint('property_bp', __name__)
estimate_bp = Blueprint('estimate_bp', __name__)

from . import property_routes, estimate_routes
