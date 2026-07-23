"""SOS routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_guest, handle_exceptions
from utils.validators import validate_location
import logging

logger = logging.getLogger(__name__)
sos_bp = Blueprint("sos", __name__)


@sos_bp.route("/sos", methods=["POST"])
@require_guest
@handle_exceptions
def trigger_sos():
    """Trigger SOS alert.
    
    Request JSON:
        - latitude: User latitude
        - longitude: User longitude
        - emergency_type: Type of emergency
        - description: Emergency description
    
    Returns:
        SOS status and notification confirmation
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        latitude = float(data.get("latitude"))
        longitude = float(data.get("longitude"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    # Validate location
    is_valid, error = validate_location(latitude, longitude)
    if not is_valid:
        return jsonify({"error": error}), 400

    emergency_type = data.get("emergency_type", "Unknown")
    description = data.get("description", "")

    try:
        from services.sos_service import trigger_sos_alert
        from datetime import datetime
        import uuid

        sos_id = str(uuid.uuid4())
        sos_alert = trigger_sos_alert(
            {
                "sos_id": sos_id,
                "user_id": request.user.get("uid") if request.user else None,
                "latitude": latitude,
                "longitude": longitude,
                "emergency_type": emergency_type,
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "active",
            }
        )

        logger.info(f"SOS alert triggered: {sos_id}")

        return jsonify({"message": "SOS alert activated", "sos_id": sos_id}), 201
    except Exception as e:
        logger.error(f"Error triggering SOS: {str(e)}")
        return jsonify({"error": "Failed to trigger SOS"}), 500
