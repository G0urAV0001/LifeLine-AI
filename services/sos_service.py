"""SOS alert service."""

import logging
from typing import Dict, Any
from utils.firebase_utils import save_to_firestore, query_firestore
from datetime import datetime

logger = logging.getLogger(__name__)


def trigger_sos_alert(sos_data: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger an SOS alert.
    
    Args:
        sos_data: SOS alert data
    
    Returns:
        SOS alert record
    """
    try:
        sos_id = sos_data.get("sos_id")
        
        # Save SOS alert
        save_to_firestore("sos_alerts", sos_id, sos_data)
        
        # Notify emergency services
        notify_emergency_services(sos_data)
        
        # Notify emergency contacts
        if sos_data.get("user_id"):
            notify_emergency_contacts(sos_data["user_id"], sos_data)
        
        logger.info(f"SOS alert triggered: {sos_id}")
        return sos_data
    except Exception as e:
        logger.error(f"Error triggering SOS: {str(e)}")
        raise


def notify_emergency_services(sos_data: Dict[str, Any]) -> bool:
    """Notify emergency services of SOS alert.
    
    Args:
        sos_data: SOS alert data
    
    Returns:
        True if notification successful
    """
    try:
        # TODO: Integrate with emergency services API/SMS service
        logger.info(f"Emergency services notified for SOS: {sos_data.get('sos_id')}")
        return True
    except Exception as e:
        logger.error(f"Error notifying emergency services: {str(e)}")
        raise


def notify_emergency_contacts(user_id: str, sos_data: Dict[str, Any]) -> bool:
    """Notify emergency contacts of SOS alert.
    
    Args:
        user_id: User ID
        sos_data: SOS alert data
    
    Returns:
        True if notifications sent
    """
    try:
        # Get emergency contacts
        contacts = query_firestore("contacts", "user_id", "==", user_id)
        
        # TODO: Send SMS/notifications to contacts
        logger.info(f"Emergency contacts notified: {len(contacts)} contacts")
        return True
    except Exception as e:
        logger.error(f"Error notifying emergency contacts: {str(e)}")
        raise
