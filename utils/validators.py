"""Input validation utilities for LifeLine AI."""

import re
from typing import Tuple, Optional
from flask import current_app


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email address.
    
    Args:
        email: Email address to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return False, "Invalid email format"

    if len(email) > 254:
        return False, "Email is too long"

    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password strength.
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required and must be a string"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password is too long"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"

    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate phone number.
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone or not isinstance(phone, str):
        return False, "Phone number is required and must be a string"

    phone_regex = r"^[\d\s\-\+\(\)]{7,20}$"
    if not re.match(phone_regex, phone):
        return False, "Invalid phone number format"

    return True, None


def validate_text_input(text: str) -> Tuple[bool, Optional[str]]:
    """Validate text input for AI assistant.
    
    Args:
        text: Text input to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Text input is required"

    text = text.strip()
    if len(text) == 0:
        return False, "Text input cannot be empty"

    max_length = current_app.config.get("MAX_TEXT_LENGTH", 5000)
    if len(text) > max_length:
        return False, f"Text input exceeds maximum length of {max_length} characters"

    return True, None


def validate_location(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """Validate geographic coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False, "Latitude and longitude must be numbers"

    if not (-90 <= latitude <= 90):
        return False, "Latitude must be between -90 and 90"

    if not (-180 <= longitude <= 180):
        return False, "Longitude must be between -180 and 180"

    return True, None


def sanitize_string(text: str) -> str:
    """Sanitize string input to prevent injection attacks.
    
    Args:
        text: Text to sanitize
    
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""

    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", '"', "'", "&", ";"]
    for char in dangerous_chars:
        text = text.replace(char, "")

    return text.strip()


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed.
    
    Args:
        filename: Filename to check
    
    Returns:
        True if file is allowed
    """
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    allowed_extensions = current_app.config.get("ALLOWED_EXTENSIONS", set())
    return extension in allowed_extensions
