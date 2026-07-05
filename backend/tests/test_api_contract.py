"""
Guards against silently drifting away from the frontend's api_client.py
contract (see companion repo README). If this test starts failing, someone
changed a route/method that the frontend depends on.
"""
from app.main import app

EXPECTED_ROUTES = {
    ("POST", "/api/experiments"),
    ("GET", "/api/experiments"),
    ("GET", "/api/experiments/{experiment_id}"),
    ("PUT", "/api/experiments/{experiment_id}"),
    ("DELETE", "/api/experiments/{experiment_id}"),
    ("POST", "/api/personas/generate"),
    ("GET", "/api/personas/experiment/{experiment_id}"),
    ("GET", "/api/personas/{persona_id}"),
}


def test_api_matches_frontend_contract():
    actual_routes = set()
    for route in app.routes:
        if not hasattr(route, "methods"):
            continue
        for method in route.methods:
            if method in ("HEAD", "OPTIONS"):
                continue
            actual_routes.add((method, route.path))

    missing = EXPECTED_ROUTES - actual_routes
    assert not missing, f"Frontend-expected routes missing from backend: {missing}"
