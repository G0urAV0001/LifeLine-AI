"""Emergency history routes for LifeLine AI."""

from flask import Blueprint, request, jsonify
from utils.decorators import require_auth, handle_exceptions
from utils.firebase_utils import query_firestore
import logging

logger = logging.getLogger(__name__)
history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
@require_auth
@handle_exceptions
def get_emergency_history():
    """Get user's emergency request history.
    
    Query Parameters:
        - limit: Number of records to return (default 50, max 100)
        - offset: Offset for pagination (default 0)
    
    Returns:
        List of emergency requests with AI responses
    """
    uid = request.user["uid"]
    limit = min(int(request.args.get("limit", 50)), 100)
    offset = int(request.args.get("offset", 0))

    try:
        # Query emergency history
        history = query_firestore("emergency_history", "user_id", "==", uid)

        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # Apply pagination
        total = len(history)
        history = history[offset : offset + limit]

        logger.info(f"Retrieved {len(history)} history records for user: {uid}")

        return (
            jsonify({
                "history": history,
                "count": len(history),
                "total": total,
                "limit": limit,
                "offset": offset,
            }),
            200,
        )
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return jsonify({"error": "Failed to retrieve history"}), 500
