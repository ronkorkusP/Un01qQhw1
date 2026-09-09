"""
Vehicle Service API
-------------------
A Flask application implementing the Vehicle Service API with in-memory storage.
Requires an API key via the X-API-Key header on all routes.

Python 3.14+ compatible.
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# API key for authentication. Override via the API_KEY environment variable.
API_KEY = os.environ.get("API_KEY", "postman-rocks")

# Port to listen on. Override via the PORT environment variable.
PORT = int(os.environ.get("PORT", 5000))

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

# vehicles: dict[int, dict]  — keyed by auto-incremented integer ID
vehicles: dict = {}
_next_id: int = 1  # auto-increment counter


def _next_vehicle_id() -> int:
    """Return the next available vehicle ID and advance the counter."""
    global _next_id
    vid = _next_id
    _next_id += 1
    return vid


# ---------------------------------------------------------------------------
# Authentication helper
# ---------------------------------------------------------------------------

def _check_api_key() -> bool:
    """Return True if the request carries a valid API key."""
    return request.headers.get("X-API-Key") == API_KEY


def _unauthorized():
    """Return a 401 Unauthorized JSON response."""
    return jsonify({"error": "Unauthorized – missing or invalid API key"}), 401


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/vehicles", methods=["POST"])
def create_vehicle():
    """
    POST /vehicles
    Create a new vehicle.

    Required body fields: nickName, vin, make, model, year, miles
    Returns 201 on success, 400 if required fields are missing,
    409 if a vehicle with the same VIN already exists.
    """
    if not _check_api_key():
        return _unauthorized()

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Validate required fields
    required_fields = ["nickName", "vin", "make", "model", "year", "miles"]
    missing = [f for f in required_fields if f not in data or data[f] is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Validate field types
    if not isinstance(data["miles"], int):
        return jsonify({"error": "'miles' must be an integer"}), 400

    # Check for duplicate VIN
    vin = str(data["vin"])
    for v in vehicles.values():
        if v["vin"] == vin:
            return jsonify({"error": "A vehicle with the same VIN already exists"}), 409

    # Persist the new vehicle
    vid = _next_vehicle_id()
    vehicle = {
        "id":       vid,
        "nickName": str(data["nickName"]),
        "vin":      vin,
        "make":     str(data["make"]),
        "model":    str(data["model"]),
        "year":     str(data["year"]),
        "miles":    int(data["miles"]),
    }
    vehicles[vid] = vehicle

    return jsonify(vehicle), 201


@app.route("/vehicles", methods=["GET"])
def get_all_vehicles():
    """
    GET /vehicles
    Return a list of all vehicles.

    Returns 200 with an array (empty if no vehicles exist).
    """
    if not _check_api_key():
        return _unauthorized()

    return jsonify(list(vehicles.values())), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id: int):
    """
    GET /vehicles/<id>
    Retrieve a single vehicle by its integer ID.

    Returns 200 on success, 404 if the vehicle does not exist.
    """
    if not _check_api_key():
        return _unauthorized()

    vehicle = vehicles.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": f"Vehicle ID {vehicle_id} does not exist"}), 404

    return jsonify(vehicle), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["PATCH"])
def update_vehicle(vehicle_id: int):
    """
    PATCH /vehicles/<id>
    Partially update an existing vehicle.

    Accepts any subset of the vehicle fields.
    Returns 200 on success, 400 if the body is invalid,
    404 if the vehicle does not exist.
    """
    if not _check_api_key():
        return _unauthorized()

    vehicle = vehicles.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": f"Vehicle ID {vehicle_id} does not exist"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Allowed mutable fields (id is immutable)
    allowed_fields = {"nickName", "vin", "make", "model", "year", "miles"}
    unknown = set(data.keys()) - allowed_fields
    if unknown:
        return jsonify({"error": f"Unknown fields: {', '.join(sorted(unknown))}"}), 400

    # Validate miles type if provided
    if "miles" in data and not isinstance(data["miles"], int):
        return jsonify({"error": "'miles' must be an integer"}), 400

    # Check for VIN conflict if vin is being changed
    if "vin" in data:
        new_vin = str(data["vin"])
        for vid, v in vehicles.items():
            if v["vin"] == new_vin and vid != vehicle_id:
                return jsonify({"error": "A vehicle with the same VIN already exists"}), 409
        vehicle["vin"] = new_vin

    # Apply updates
    for field in allowed_fields - {"vin"}:
        if field in data:
            vehicle[field] = int(data[field]) if field == "miles" else str(data[field])

    return jsonify(vehicle), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id: int):
    """
    DELETE /vehicles/<id>
    Delete a vehicle by its integer ID.

    Returns 204 No Content on success, 404 if the vehicle does not exist.
    """
    if not _check_api_key():
        return _unauthorized()

    if vehicle_id not in vehicles:
        return jsonify({"error": f"Vehicle ID {vehicle_id} does not exist"}), 404

    del vehicles[vehicle_id]
    return "", 204


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested resource was not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Unexpected server-side failure"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Starting Vehicle Service API on port {PORT}")
    print(f"API key: {API_KEY}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
