from flask import Flask, request, jsonify
from flask_cors import CORS
from model_utils import generate_title
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # Allow React frontend (localhost:5173) to call Flask API

@app.get("/")
def home():
    return jsonify({"message": "API running"})

@app.post("/generate_title")
def generate_title_api():
    data = request.get_json(force=True) or {}
    story_text = (data.get("story_text") or "").strip()
    image_b64 = data.get("image_base64")
    reference_title = (data.get("reference_title") or "").strip()

    if not story_text and not image_b64:
        return jsonify({"error": "Please provide either story_text or image_base64."}), 400

    # Decode image if provided
    pil_image = None
    if image_b64:
        try:
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            image_bytes = base64.b64decode(image_b64)
            pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return jsonify({"error": f"Invalid image data: {e}"}), 400

    # Generate title and optional BERTScore
    try:
        result = generate_title(story_text, image_b64, reference_title)
        return jsonify(result)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed to generate title: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
