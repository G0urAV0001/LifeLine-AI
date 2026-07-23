"""Application configuration."""

import os
from datetime import timedelta


class Config:
    """Base configuration."""

    # Flask config
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", False)
    TESTING = False
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Firebase config
    FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL")
    FIREBASE_DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL")
    FIREBASE_STORAGE_BUCKET = os.environ.get("FIREBASE_STORAGE_BUCKET")
    
    # App config
    MAX_TEXT_LENGTH = 5000
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp3", "wav"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # CORS config
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
