"""Authentication utilities for LifeLine AI."""

import firebase_admin
from firebase_admin import auth as firebase_auth
from flask import current_app
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


def verify_firebase_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase ID token.
    
    Args:
        token: Firebase ID token
    
    Returns:
        Decoded token claims or None if invalid
    
    Raises:
        Exception: If token verification fails
    """
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except firebase_auth.ExpiredSignInError:
        logger.warning("Token expired")
        raise ValueError("Token has expired")
    except firebase_auth.RevokedSignInError:
        logger.warning("Token revoked")
        raise ValueError("Token has been revoked")
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}")


def verify_session_cookie(session_cookie: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase session cookie.
    
    Args:
        session_cookie: Session cookie from user
    
    Returns:
        Decoded claims or None if invalid
    """
    try:
        decoded_claims = firebase_auth.verify_session_cookie(
            session_cookie, check_revoked=True
        )
        return decoded_claims
    except firebase_auth.ExpiredSessionCookieError:
        logger.warning("Session cookie expired")
        raise ValueError("Session cookie has expired")
    except firebase_auth.RevokedSessionCookieError:
        logger.warning("Session cookie revoked")
        raise ValueError("Session cookie has been revoked")
    except Exception as e:
        logger.error(f"Session cookie verification error: {str(e)}")
        raise ValueError(f"Invalid session: {str(e)}")


def create_session_cookie(id_token: str, expires_in: int = 3600 * 24 * 5) -> str:
    """Create a session cookie from an ID token.
    
    Args:
        id_token: Firebase ID token
        expires_in: Session duration in seconds (default 5 days)
    
    Returns:
        Session cookie string
    """
    try:
        session_cookie = firebase_auth.create_session_cookie(id_token, expires_in=expires_in)
        return session_cookie
    except Exception as e:
        logger.error(f"Error creating session cookie: {str(e)}")
        raise


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email address.
    
    Args:
        email: User email
    
    Returns:
        User data or None if not found
    """
    try:
        user = firebase_auth.get_user_by_email(email)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "email_verified": user.email_verified,
        }
    except firebase_auth.UserNotFoundError:
        logger.warning(f"User not found: {email}")
        return None
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise


def update_user_profile(uid: str, display_name: Optional[str] = None, photo_url: Optional[str] = None) -> bool:
    """Update user profile.
    
    Args:
        uid: User ID
        display_name: New display name
        photo_url: New photo URL
    
    Returns:
        True if successful
    """
    try:
        firebase_auth.update_user(
            uid,
            display_name=display_name,
            photo_url=photo_url,
        )
        logger.info(f"User profile updated: {uid}")
        return True
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise


def reset_password(email: str) -> bool:
    """Send password reset email.
    
    Args:
        email: User email
    
    Returns:
        True if successful
    """
    try:
        firebase_auth.generate_password_reset_link(email)
        logger.info(f"Password reset email sent to: {email}")
        return True
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        raise


def delete_user(uid: str) -> bool:
    """Delete a user account.
    
    Args:
        uid: User ID
    
    Returns:
        True if successful
    """
    try:
        firebase_auth.delete_user(uid)
        logger.info(f"User deleted: {uid}")
        return True
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise
