import os
from typing import Any, Dict
import requests



routing_server_hostname = os.environ['ROUTING_HOST']


def get_route_qurey_template() -> Dict[Any, Any]:
    return {
        "points": [],
        "profile": "bike",
        "elevation": True,
        "instructions": True,
        "locale": "ru_RU",
        "points_encoded": False,
        "snap_preventions": [
            "ferry"
        ],
        "details": [
            "road_class",
            "road_environment",
            "max_speed",
            "average_speed"
        ]
    }

def get_route(start: tuple[float, float], dest: tuple[float, float]) -> Dict[Any, Any]:
    url = routing_server_hostname + "route?key="
    body = get_route_qurey_template()
    body['points'] = [list(start), list(dest)]
    return requests.post(url, json=body).json()

