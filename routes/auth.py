"""Authentication routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.validators import validate_email, validate_password
from utils.firebase_utils import create_user, get_user
from utils.auth_utils import verify_firebase_token, create_session_cookie, get_user_by_email
from utils.decorators import handle_exceptions
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
@handle_exceptions
def signup():
    """User signup endpoint.
    
    Request JSON:
        - email: User email
        - password: User password
        - display_name: Optional display name
    
    Returns:
        User data and session cookie
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")
    display_name = data.get("display_name", "").strip()

    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate password
    is_valid, error = validate_password(password)
    if not is_valid:
        return jsonify({"error": error}), 400

    try:
        # Create user
        user = create_user(email, password, display_name or None)
        logger.info(f"User signed up: {user['uid']}")

        return (
            jsonify({
                "message": "Signup successful",
                "user": user,
            }),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({"error": "Signup failed"}), 500


@auth_bp.route("/login", methods=["POST"])
@handle_exceptions
def login():
    """User login endpoint.
    
    Request JSON:
        - email: User email
        - password: User password
        - id_token: Firebase ID token (from client-side auth)
    
    Returns:
        User data and session cookie
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    id_token = data.get("id_token")

    if not id_token:
        return jsonify({"error": "ID token is required"}), 400

    try:
        # Verify token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token["uid"]

        # Get user data
        user_data = get_user(uid)
        if not user_data:
            return jsonify({"error": "User not found"}), 404

        # Create session cookie
        session_cookie = create_session_cookie(id_token)

        logger.info(f"User logged in: {uid}")

        return (
            jsonify({
                "message": "Login successful",
                "user": user_data,
                "session_cookie": session_cookie,
            }),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route("/guest", methods=["POST"])
@handle_exceptions
def guest_login():
    """Guest login endpoint.
    
    Returns:
        Guest session token
    """
    import uuid
    from datetime import datetime

    try:
        guest_id = str(uuid.uuid4())
        guest_token = f"guest_{guest_id}"

        logger.info(f"Guest session created: {guest_id}")

        return (
            jsonify({
                "message": "Guest session created",
                "guest_id": guest_id,
                "guest_token": guest_token,
                "created_at": datetime.utcnow().isoformat(),
            }),
            201,
        )
    except Exception as e:
        logger.error(f"Guest login error: {str(e)}")
        return jsonify({"error": "Guest login failed"}), 500


@auth_bp.route("/logout", methods=["POST"])
@handle_exceptions
def logout():
    """User logout endpoint.
    
    Returns:
        Logout confirmation
    """
    try:
        logger.info("User logged out")
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"error": "Logout failed"}), 500


@auth_bp.route("/verify-token", methods=["POST"])
@handle_exceptions
def verify_token():
    """Verify Firebase token.
    
    Request JSON:
        - token: Firebase ID token
    
    Returns:
        Token validity and user claims
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded_token = verify_firebase_token(token)
        return (
            jsonify({
                "valid": True,
                "user_id": decoded_token["uid"],
                "email": decoded_token.get("email"),
            }),
            200,
        )
    except ValueError as e:
        return jsonify({"valid": False, "error": str(e)}), 401
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({"error": "Token verification failed"}), 500


@auth_bp.route("/reset-password", methods=["POST"])
@handle_exceptions
def reset_password():
    """Send password reset email.
    
    Request JSON:
        - email: User email
    
    Returns:
        Reset email sent confirmation
    """
    from utils.auth_utils import reset_password as send_reset_email

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email", "").strip()

    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        return jsonify({"error": error}), 400

    try:
        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            # Don't reveal if email exists
            return (
                jsonify({"message": "If the email exists, a reset link has been sent"}),
                200,
            )

        send_reset_email(email)
        logger.info(f"Password reset email sent to: {email}")

        return (
            jsonify({"message": "Password reset email sent"}),
            200,
        )
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({"error": "Password reset failed"}), 500
