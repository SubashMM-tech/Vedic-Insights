from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
import vedastro

# --- Configuration ---
app = Flask(__name__)
CORS(app)

# --- Data Validation Model ---
class BirthData(BaseModel):
    name: str
    date: str  # Expecting "YYYY-MM-DD"
    time: str  # Expecting "HH:MM"
    lat: float
    lng: float

# --- API Endpoints ---
@app.route("/")
def home():
    return "Vedic Insights Jyotish API is online."

@app.route("/calculate", methods=['POST'])
def calculate_chart():
    try:
        # 1. Validate the incoming data
        validated_data = BirthData(**request.json)

        # 2. Create the Time object for calculation
        time_obj = vedastro.Time(
            f"{validated_data.date} {validated_data.time}",
            vedastro.GeoLocation(latitude=validated_data.lat, longitude=validated_data.lng)
        )

        # 3. Perform REAL astrological calculations
        response = {
            "status": "success",
            "Lagna": vedastro.House.First(time_obj).GetSignName(),
            "Moon Sign": vedastro.Moon(time_obj).GetSignName(),
            "Nakshatra": vedastro.Moon(time_obj).GetNakshatraName(),
            "planets": {
                "Sun": vedastro.Sun(time_obj).GetSignName(),
                "Moon": vedastro.Moon(time_obj).GetSignName(),
                "Mars": vedastro.Mars(time_obj).GetSignName(),
                "Mercury": vedastro.Mercury(time_obj).GetSignName(),
                "Jupiter": vedastro.Jupiter(time_obj).GetSignName(),
                "Venus": vedastro.Venus(time_obj).GetSignName(),
                "Saturn": vedastro.Saturn(time_obj).GetSignName()
            }
        }
        
        # 4. Send the successful response
        return jsonify(response)

    except ValidationError as e:
        return jsonify({"status": "error", "message": f"Invalid input: {e.errors()}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Calculation error: {str(e)}"}), 500
