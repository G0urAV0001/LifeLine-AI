"""User profile routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_auth, handle_exceptions
from utils.firebase_utils import get_from_firestore, save_to_firestore
from utils.auth_utils import update_user_profile, get_user
import logging

logger = logging.getLogger(__name__)
profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@require_auth
@handle_exceptions
def get_profile():
    """Get user profile.
    
    Returns:
        User profile data
    """
    uid = request.user["uid"]

    try:
        # Get user from Firebase Auth
        user_data = get_user(uid)
        if not user_data:
            return jsonify({"error": "User not found"}), 404

        # Get profile from Firestore
        profile = get_from_firestore("users", uid)

        # Merge data
        if profile:
            user_data.update(profile)

        logger.info(f"Profile retrieved for user: {uid}")
        return jsonify(user_data), 200
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        return jsonify({"error": "Failed to retrieve profile"}), 500


@profile_bp.route("/profile", methods=["PUT"])
@require_auth
@handle_exceptions
def update_profile():
    """Update user profile.
    
    Request JSON:
        - display_name: Optional display name
        - photo_url: Optional photo URL
        - phone: Optional phone number
        - emergency_contacts: Optional emergency contacts
    
    Returns:
        Updated profile data
    """
    uid = request.user["uid"]
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Update Firebase Auth fields
        display_name = data.get("display_name")
        photo_url = data.get("photo_url")

        if display_name or photo_url:
            update_user_profile(uid, display_name, photo_url)

        # Update Firestore profile
        profile_data = {k: v for k, v in data.items() if v is not None}
        profile_data["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()

        save_to_firestore("users", uid, profile_data)

        logger.info(f"Profile updated for user: {uid}")
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        return jsonify({"error": "Failed to update profile"}), 500
