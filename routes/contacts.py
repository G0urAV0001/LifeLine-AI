"""Emergency contacts routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_auth, handle_exceptions
from utils.validators import validate_phone, validate_email
from utils.firebase_utils import save_to_firestore, get_from_firestore, delete_from_firestore, query_firestore
import logging
import uuid

logger = logging.getLogger(__name__)
contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/contacts", methods=["GET"])
@require_auth
@handle_exceptions
def get_contacts():
    """Get user's emergency contacts.
    
    Returns:
        List of emergency contacts
    """
    uid = request.user["uid"]

    try:
        contacts = query_firestore("contacts", "user_id", "==", uid)
        logger.info(f"Retrieved {len(contacts)} contacts for user: {uid}")

        return jsonify({"contacts": contacts, "count": len(contacts)}), 200
    except Exception as e:
        logger.error(f"Error retrieving contacts: {str(e)}")
        return jsonify({"error": "Failed to retrieve contacts"}), 500


@contacts_bp.route("/contacts", methods=["POST"])
@require_auth
@handle_exceptions
def create_contact():
    """Create a new emergency contact.
    
    Request JSON:
        - name: Contact name
        - phone: Contact phone number
        - email: Optional contact email
        - relationship: Relationship to user
    
    Returns:
        Created contact data
    """
    uid = request.user["uid"]
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    relationship = data.get("relationship", "").strip()

    # Validate inputs
    if not name:
        return jsonify({"error": "Contact name is required"}), 400

    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    is_valid, error = validate_phone(phone)
    if not is_valid:
        return jsonify({"error": error}), 400

    if email:
        is_valid, error = validate_email(email)
        if not is_valid:
            return jsonify({"error": error}), 400

    try:
        contact_id = str(uuid.uuid4())
        contact_data = {
            "id": contact_id,
            "user_id": uid,
            "name": name,
            "phone": phone,
            "email": email or None,
            "relationship": relationship,
            "created_at": __import__("datetime").datetime.utcnow().isoformat(),
        }

        save_to_firestore("contacts", contact_id, contact_data)
        logger.info(f"Contact created: {contact_id}")

        return jsonify({"message": "Contact created", "contact": contact_data}), 201
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}")
        return jsonify({"error": "Failed to create contact"}), 500


@contacts_bp.route("/contacts/<contact_id>", methods=["PUT"])
@require_auth
@handle_exceptions
def update_contact(contact_id):
    """Update an emergency contact.
    
    Args:
        contact_id: Contact ID
    
    Request JSON:
        - name: Contact name
        - phone: Contact phone number
        - email: Contact email
        - relationship: Relationship to user
    
    Returns:
        Updated contact data
    """
    uid = request.user["uid"]
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Verify contact belongs to user
        contact = get_from_firestore("contacts", contact_id)
        if not contact or contact.get("user_id") != uid:
            return jsonify({"error": "Contact not found"}), 404

        # Validate and update fields
        update_data = {}

        if "name" in data:
            update_data["name"] = data["name"].strip()

        if "phone" in data:
            phone = data["phone"].strip()
            is_valid, error = validate_phone(phone)
            if not is_valid:
                return jsonify({"error": error}), 400
            update_data["phone"] = phone

        if "email" in data:
            email = data["email"].strip()
            if email:
                is_valid, error = validate_email(email)
                if not is_valid:
                    return jsonify({"error": error}), 400
            update_data["email"] = email or None

        if "relationship" in data:
            update_data["relationship"] = data["relationship"].strip()

        update_data["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()

        save_to_firestore("contacts", contact_id, update_data)
        logger.info(f"Contact updated: {contact_id}")

        return jsonify({"message": "Contact updated"}), 200
    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        return jsonify({"error": "Failed to update contact"}), 500


@contacts_bp.route("/contacts/<contact_id>", methods=["DELETE"])
@require_auth
@handle_exceptions
def delete_contact(contact_id):
    """Delete an emergency contact.
    
    Args:
        contact_id: Contact ID
    
    Returns:
        Deletion confirmation
    """
    uid = request.user["uid"]

    try:
        # Verify contact belongs to user
        contact = get_from_firestore("contacts", contact_id)
        if not contact or contact.get("user_id") != uid:
            return jsonify({"error": "Contact not found"}), 404

        delete_from_firestore("contacts", contact_id)
        logger.info(f"Contact deleted: {contact_id}")

        return jsonify({"message": "Contact deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting contact: {str(e)}")
        return jsonify({"error": "Failed to delete contact"}), 500
