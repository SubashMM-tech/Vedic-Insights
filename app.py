from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
import vedastro  # This is the modern Vedic astrology library

# Initialize the Flask web application
app = Flask(__name__)
# Allow requests from your Firebase Studio app URL (and others)
CORS(app)

# Define the structure of the incoming data to prevent errors
class BirthData(BaseModel):
    name: str  # <-- ADD THIS LINE
    date: str
    time: str
    lat: float
    lng: float

@app.route("/")
def home():
    # A simple home page to confirm the service is running
    return "Jyotish API is online and running."

@app.route("/calculate", methods=['POST'])
def calculate_chart():
    try:
        # Get the JSON data sent by your Next.js app
        data = request.json
        # Validate the incoming data against our model
        birth_data = BirthData(**data)
        
        # Create the vedastro objects
        time_obj = vedastro.Time(f"{birth_data.date} {birth_data.time}", vedastro.GeoLocation(latitude=birth_data.lat, longitude=birth_data.lng))

        # --- Perform the Calculations ---
        lagna = vedastro.House.First(time_obj).GetSignName()
        moon_sign = vedastro.Moon(time_obj).GetSignName()
        moon_nakshatra = vedastro.Moon(time_obj).GetNakshatraName()
        
        # Calculate planet positions
        planets_data = {
            "Sun": vedastro.Sun(time_obj).GetSignName(),
            "Moon": moon_sign,
            "Mars": vedastro.Mars(time_obj).GetSignName(),
            "Mercury": vedastro.Mercury(time_obj).GetSignName(),
            "Jupiter": vedastro.Jupiter(time_obj).GetSignName(),
            "Venus": vedastro.Venus(time_obj).GetSignName(),
            "Saturn": vedastro.Saturn(time_obj).GetSignName(),
        }

        # --- Prepare the Successful Response ---
        # The structure of this response matches what your Next.js app expects
        response = {
            "status": "success",
            "Lagna": lagna,
            "Moon Sign": moon_sign,
            "Nakshatra": moon_nakshatra,
            "planets": planets_data
        }
        return jsonify(response)

    except ValidationError as e:
        # If data is missing or wrong type
        return jsonify({"status": "error", "message": "Invalid input data.", "details": e.errors()}), 400
    except Exception as e:
        # For any other calculation errors
        return jsonify({"status": "error", "message": "An error occurred during calculation.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
