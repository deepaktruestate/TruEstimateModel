from flask import Blueprint, request, jsonify
from truEstimate.services import EstimateService

estimate_bp = Blueprint('estimate_bp', __name__)
estimate_service = EstimateService('truEstimate/data/rtm_properties.json')

SIMILARITY_THRESHOLD = 0.6

@estimate_bp.route('/truestimate', methods=['POST'])
def truestimate():
    new_property = request.get_json()
    if not new_property:
        return jsonify({"error": "No property data provided"}), 400

    price = estimate_service.estimate_price(new_property, similarity_threshold=SIMILARITY_THRESHOLD)
    if price is None:
        return jsonify({"error": "No sufficiently similar properties found"}), 404

    return jsonify({"estimated_price_per_sqft": price})
