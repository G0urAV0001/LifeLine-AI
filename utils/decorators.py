"""Custom decorators for LifeLine AI."""

from functools import wraps
from flask import request, jsonify, current_app
from utils.auth_utils import verify_firebase_token
import logging

logger = logging.getLogger(__name__)


def require_auth(f):
    """Decorator to require Firebase authentication.
    
    Args:
        f: Flask route function
    
    Returns:
        Decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid authorization header"}), 401

        if not token:
            return jsonify({"error": "Authorization required"}), 401

        try:
            user = verify_firebase_token(token)
            request.user = user
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Authentication failed: {str(e)}")
            return jsonify({"error": "Invalid or expired token"}), 401

    return decorated_function


def require_guest(f):
    """Decorator to allow guest access.
    
    Args:
        f: Flask route function
    
    Returns:
        Decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        request.user = None

        # Get token from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
                user = verify_firebase_token(token)
                request.user = user
            except Exception as e:
                logger.warning(f"Token verification failed: {str(e)}")
                # Continue with guest access

        return f(*args, **kwargs)

    return decorated_function


def rate_limit(requests_per_period=None):
    """Decorator to implement rate limiting.
    
    Args:
        requests_per_period: Number of requests allowed per period
    
    Returns:
        Decorated function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO: Implement rate limiting with Redis or in-memory store
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def handle_exceptions(f):
    """Decorator to handle exceptions gracefully.
    
    Args:
        f: Flask route function
    
    Returns:
        Decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    return decorated_function
