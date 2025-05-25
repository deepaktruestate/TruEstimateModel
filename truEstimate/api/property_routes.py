from flask import Blueprint, request, jsonify
from truEstimate.services import PropertyService
from truEstimate.models import Preprocessor


property_bp = Blueprint('property_bp', __name__)

# Instantiate preprocessor and pass to service
preprocessor = Preprocessor({'cagr':[0,15],'projectLandArea':[0,100]})
property_service = PropertyService('truEstimate/data/rtm_properties.json', preprocessor=preprocessor)

@property_bp.route('/addProperty', methods=['POST'])
def add_property():
    new_property = request.get_json()
    if not new_property:
        return jsonify({"error": "No property data provided"}), 400

    success = property_service.add_property(new_property)
    if not success:
        return jsonify({"error": "Property already exists or invalid data"}), 400

    return jsonify({"message": "Property added successfully"}), 201

@property_bp.route('/deleteProperty/<property_id>', methods=['DELETE'])
def delete_property(property_id):
    success = property_service.delete_property(property_id)
    if not success:
        return jsonify({"error": "Property not found"}), 404

    return jsonify({"message": "Property deleted successfully"})

@property_bp.route('/updateProperty/<property_id>', methods=['PUT'])
def update_property(property_id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No update data provided"}), 400

    success = property_service.update_property(property_id, update_data)
    if not success:
        return jsonify({"error": "Property not found or invalid update data"}), 404

    return jsonify({"message": "Property updated successfully"})
