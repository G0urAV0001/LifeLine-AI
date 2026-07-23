"""AI Assistant routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_guest, handle_exceptions
from utils.validators import validate_text_input
import logging

logger = logging.getLogger(__name__)
ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/text", methods=["POST"])
@require_guest
@handle_exceptions
def process_text():
    """Process text input through AI assistant.
    
    Request JSON:
        - text: Text input describing the emergency
    
    Returns:
        AI analysis with emergency guidance
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    text = data.get("text", "").strip()

    # Validate input
    is_valid, error = validate_text_input(text)
    if not is_valid:
        return jsonify({"error": error}), 400

    try:
        from services.ai_service import process_emergency_text

        result = process_emergency_text(text, request.user)
        logger.info("Text input processed successfully")

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        return jsonify({"error": "Failed to process text"}), 500


@ai_bp.route("/image", methods=["POST"])
@require_guest
@handle_exceptions
def process_image():
    """Process image input through AI assistant.
    
    Request Form Data:
        - image: Image file
        - description: Optional text description
    
    Returns:
        AI analysis of the image
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    description = request.form.get("description", "")

    if image.filename == "":
        return jsonify({"error": "No image selected"}), 400

    try:
        from services.ai_service import process_emergency_image

        result = process_emergency_image(image, description, request.user)
        logger.info("Image processed successfully")

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": "Failed to process image"}), 500


@ai_bp.route("/voice", methods=["POST"])
@require_guest
@handle_exceptions
def process_voice():
    """Process voice transcript through AI assistant.
    
    Request JSON:
        - transcript: Voice transcript text
        - language: Optional language code
    
    Returns:
        AI analysis of the voice input
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    transcript = data.get("transcript", "").strip()
    language = data.get("language", "en")

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    try:
        from services.ai_service import process_emergency_voice

        result = process_emergency_voice(transcript, language, request.user)
        logger.info("Voice input processed successfully")

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error processing voice: {str(e)}")
        return jsonify({"error": "Failed to process voice"}), 500
