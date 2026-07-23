"""Main Flask application for LifeLine AI."""

from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from utils.firebase_utils import initialize_firebase
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.ai import ai_bp
from routes.hospitals import hospitals_bp
from routes.sos import sos_bp
from routes.contacts import contacts_bp
from routes.history import history_bp
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Firebase
    try:
        initialize_firebase(app)
    except Exception as e:
        logger.warning(f"Firebase initialization warning: {str(e)}")

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/users")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(hospitals_bp, url_prefix="/api/emergency")
    app.register_blueprint(sos_bp, url_prefix="/api/emergency")
    app.register_blueprint(contacts_bp, url_prefix="/api/users")
    app.register_blueprint(history_bp, url_prefix="/api/users")

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy", "service": "LifeLine AI API"}), 200

    # Home endpoint
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "name": "LifeLine AI API",
            "version": "1.0.0",
            "description": "AI-powered emergency response system",
            "endpoints": {
                "health": "/api/health",
                "auth": "/api/auth",
                "profile": "/api/users",
                "ai": "/api/ai",
                "emergency": "/api/emergency",
            },
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500

    logger.info(f"Application created with config: {config_name}")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
