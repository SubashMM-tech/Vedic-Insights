from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
import os
import sys

# --- Configuration ---
app = Flask(__name__)
CORS(app)  # This allows your front-end to talk to this API

# --- Logging Setup ---
# This ensures that our print statements show up in the Render logs
def log_message(message):
    print(message, file=sys.stderr)

# --- Data Validation Model ---
# This defines the exact data structure we expect to receive
class BirthData(BaseModel):
    name: str
    date: str  # Expects "YYYY-MM-DD"
    time: str  # Expects "HH:MM"
    lat: float
    lng: float

# --- API Endpoints ---
@app.route("/")
def home():
    log_message("Home endpoint was hit. Service is online.")
    return "Vedic Insights Jyotish API is running."

@app.route("/calculate", methods=['POST'])
def calculate_chart():
    log_message("\n--- /CALCULATE ENDPOINT HIT ---")

    try:
        # 1. Get and log the raw data
        raw_data = request.json
        log_message(f"1. Received raw JSON data: {raw_data}")

        # 2. Validate the data
        validated_data = BirthData(**raw_data)
        log_message(f"2. Data validated successfully.")

        # 3. Simulate chart generation (Placeholder)
        # This replaces the vedastro library to ensure we can get a successful response
        log_message("3. Simulating chart generation...")
        chart_data = {
            "Lagna": "Libra",
            "Moon Sign": "Taurus",
            "Nakshatra": "Rohini",
            "planets": {
                "Sun": "Taurus", "Moon": "Taurus", "Mars": "Gemini",
                "Mercury": "Aries", "Jupiter": "Taurus", "Venus": "Cancer", "Saturn": "Taurus"
            }
        }
        log_message("4. Chart simulation successful.")

        # 5. Send the successful response
        response = {"status": "success", **chart_data}
        log_message(f"5. Sending success response: {response}")
        return jsonify(response)

    except ValidationError as e:
        # This runs if the incoming data is malformed
        log_message(f"!!! VALIDATION ERROR: {e.errors()}")
        return jsonify({"status": "error", "message": "Invalid input data provided."}), 400
    except Exception as e:
        # This is a catch-all for any other unexpected error
        log_message(f"!!! CRITICAL ERROR DURING CALCULATION: {e}")
        return jsonify({"status": "error", "message": "An internal server error occurred."}), 500
