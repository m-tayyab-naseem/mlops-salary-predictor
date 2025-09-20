from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = joblib.load("salary_prediction_model.pkl")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Service is healthy"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Check required fields
        required_fields = ["Age", "Gender", "Education Level", "Job Title", "Years of Experience"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert input to DataFrame
        sample_df = pd.DataFrame([data])

        # Predict
        prediction = model.predict(sample_df)[0]

        return jsonify({
            "predicted_salary": round(float(prediction), 2)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
