"""Hospital finder service."""

import logging
from typing import List, Dict, Any
from math import radians, cos, sin, asin, sqrt

logger = logging.getLogger(__name__)

# Sample hospital data - Replace with actual database/API calls
SAMPLE_HOSPITALS = [
    {
        "id": "hospital_1",
        "name": "City General Hospital",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "123 Main St, New York, NY",
        "phone": "+1-212-555-0100",
        "specialties": ["Emergency", "Trauma", "Cardiac"],
        "beds_available": 15,
        "rating": 4.5,
    },
    {
        "id": "hospital_2",
        "name": "Medical Center",
        "latitude": 40.7580,
        "longitude": -73.9855,
        "address": "456 Park Ave, New York, NY",
        "phone": "+1-212-555-0200",
        "specialties": ["Emergency", "Surgery", "Pediatrics"],
        "beds_available": 8,
        "rating": 4.2,
    },
]


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Calculate the great circle distance between two points on earth (in meters)."""
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters
    return c * r


def find_nearby_hospitals(latitude: float, longitude: float, radius: int = 5000) -> List[Dict[str, Any]]:
    """Find nearby hospitals.
    
    Args:
        latitude: User latitude
        longitude: User longitude
        radius: Search radius in meters
    
    Returns:
        List of nearby hospitals sorted by distance
    """
    try:
        nearby = []

        for hospital in SAMPLE_HOSPITALS:
            distance = haversine(
                longitude,
                latitude,
                hospital["longitude"],
                hospital["latitude"],
            )

            if distance <= radius:
                hospital_data = hospital.copy()
                hospital_data["distance"] = int(distance)
                nearby.append(hospital_data)

        # Sort by distance
        nearby.sort(key=lambda x: x["distance"])

        logger.info(f"Found {len(nearby)} nearby hospitals")
        return nearby
    except Exception as e:
        logger.error(f"Error finding nearby hospitals: {str(e)}")
        raise
