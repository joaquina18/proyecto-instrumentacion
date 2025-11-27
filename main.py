from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # ← habilita conexión desde GitHub Pages

@app.route("/")
def home():
    return "ECG HRV API is running"

@app.route("/process_rr", methods=["POST"])
def process_rr():
    data = request.get_json()

    if "rr" not in data:
        return jsonify({"error": "Missing rr array"}), 400

    rr = np.array(data["rr"])

    if len(rr) < 2:
        return jsonify({"bpm": None, "rmssd": None, "sdnn": None})

    bpm = 60000 / np.mean(rr)

    diff = np.diff(rr)
    rmssd = np.sqrt(np.mean(diff**2))

    sdnn = np.std(rr)

    return jsonify({
        "bpm": round(float(bpm), 2),
        "rmssd": round(float(rmssd), 2),
        "sdnn": round(float(sdnn), 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
