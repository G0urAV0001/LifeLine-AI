"""Hospital finder routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_guest, handle_exceptions
from utils.validators import validate_location
import logging

logger = logging.getLogger(__name__)
hospitals_bp = Blueprint("hospitals", __name__)


@hospitals_bp.route("/hospitals", methods=["GET"])
@require_guest
@handle_exceptions
def find_hospitals():
    """Find nearby hospitals.
    
    Query Parameters:
        - latitude: User latitude
        - longitude: User longitude
        - radius: Search radius in meters (default 5000)
    
    Returns:
        List of nearby hospitals with details
    """
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    # Validate coordinates
    is_valid, error = validate_location(latitude, longitude)
    if not is_valid:
        return jsonify({"error": error}), 400

    radius = request.args.get("radius", 5000, type=int)

    if radius < 100 or radius > 50000:
        return jsonify({"error": "Radius must be between 100 and 50000 meters"}), 400

    try:
        from services.hospital_service import find_nearby_hospitals

        hospitals = find_nearby_hospitals(latitude, longitude, radius)
        logger.info(f"Found {len(hospitals)} nearby hospitals")

        return jsonify({"hospitals": hospitals, "count": len(hospitals)}), 200
    except Exception as e:
        logger.error(f"Error finding hospitals: {str(e)}")
        return jsonify({"error": "Failed to find hospitals"}), 500
