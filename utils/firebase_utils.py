"""Firebase utilities for authentication and database operations."""

import firebase_admin
from firebase_admin import credentials, db, auth as firebase_auth, storage
from flask import current_app
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

_db_instance = None
_auth_instance = None
_storage_instance = None


def initialize_firebase(app):
    """Initialize Firebase Admin SDK.
    
    Args:
        app: Flask application instance
    """
    global _db_instance, _auth_instance, _storage_instance

    try:
        # Check if already initialized
        if not firebase_admin._apps:
            # Build credentials dictionary from config
            cred_dict = {
                "type": "service_account",
                "project_id": app.config["FIREBASE_PROJECT_ID"],
                "private_key_id": "key123",
                "private_key": app.config["FIREBASE_PRIVATE_KEY"],
                "client_email": app.config["FIREBASE_CLIENT_EMAIL"],
                "client_id": "123456789",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/certificates",
            }

            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(
                cred,
                {
                    "databaseURL": app.config["FIREBASE_DATABASE_URL"],
                    "storageBucket": app.config["FIREBASE_STORAGE_BUCKET"],
                },
            )
            logger.info("Firebase Admin SDK initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise


def get_db():
    """Get Firebase Realtime Database instance.
    
    Returns:
        Firebase database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = db.reference()
    return _db_instance


def get_auth():
    """Get Firebase Authentication instance.
    
    Returns:
        Firebase auth instance
    """
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = firebase_auth
    return _auth_instance


def get_storage():
    """Get Firebase Storage instance.
    
    Returns:
        Firebase storage bucket
    """
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = storage.bucket()
    return _storage_instance


def create_user(email: str, password: str, display_name: Optional[str] = None) -> Dict[str, Any]:
    """Create a new user with Firebase Authentication.
    
    Args:
        email: User email address
        password: User password
        display_name: Optional display name
    
    Returns:
        Dictionary with user data including uid
    
    Raises:
        Exception: If user creation fails
    """
    try:
        auth = get_auth()
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
        )
        logger.info(f"User created: {user.uid}")
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
        }
    except firebase_auth.EmailAlreadyExistsError:
        logger.warning(f"Email already exists: {email}")
        raise ValueError("Email already registered")
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise


def get_user(uid: str) -> Optional[Dict[str, Any]]:
    """Get user by UID.
    
    Args:
        uid: Firebase user ID
    
    Returns:
        User data or None if not found
    """
    try:
        auth = get_auth()
        user = auth.get_user(uid)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
        }
    except firebase_auth.UserNotFoundError:
        logger.warning(f"User not found: {uid}")
        return None
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise


def save_to_firestore(collection: str, document_id: str, data: Dict[str, Any]) -> bool:
    """Save data to Firestore.
    
    Args:
        collection: Collection name
        document_id: Document ID
        data: Data to save
    
    Returns:
        True if successful
    """
    try:
        from firebase_admin import firestore

        db = firestore.client()
        db.collection(collection).document(document_id).set(data, merge=True)
        logger.info(f"Data saved to {collection}/{document_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving to Firestore: {str(e)}")
        raise


def get_from_firestore(collection: str, document_id: str) -> Optional[Dict[str, Any]]:
    """Get data from Firestore.
    
    Args:
        collection: Collection name
        document_id: Document ID
    
    Returns:
        Document data or None if not found
    """
    try:
        from firebase_admin import firestore

        db = firestore.client()
        doc = db.collection(collection).document(document_id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        logger.error(f"Error getting from Firestore: {str(e)}")
        raise


def delete_from_firestore(collection: str, document_id: str) -> bool:
    """Delete data from Firestore.
    
    Args:
        collection: Collection name
        document_id: Document ID
    
    Returns:
        True if successful
    """
    try:
        from firebase_admin import firestore

        db = firestore.client()
        db.collection(collection).document(document_id).delete()
        logger.info(f"Data deleted from {collection}/{document_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting from Firestore: {str(e)}")
        raise


def query_firestore(collection: str, field: str, operator: str, value: Any) -> list:
    """Query Firestore collection.
    
    Args:
        collection: Collection name
        field: Field name
        operator: Comparison operator (==, <, >, <=, >=, !=, in, array-contains)
        value: Value to compare
    
    Returns:
        List of matching documents
    """
    try:
        from firebase_admin import firestore

        db = firestore.client()
        query = db.collection(collection)

        if operator == "==":
            query = query.where(field, "==", value)
        elif operator == "<":
            query = query.where(field, "<", value)
        elif operator == ">":
            query = query.where(field, ">", value)
        elif operator == "<=":
            query = query.where(field, "<=", value)
        elif operator == ">=":
            query = query.where(field, ">=", value)
        elif operator == "!=":
            query = query.where(field, "!=", value)
        elif operator == "in":
            query = query.where(field, "in", value)
        elif operator == "array-contains":
            query = query.where(field, "array-contains", value)

        docs = query.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        logger.error(f"Error querying Firestore: {str(e)}")
        raise
