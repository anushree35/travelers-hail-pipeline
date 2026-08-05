import base64
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
api_key = os.getenv("AZURE_API_KEY")
deployment_name = "gpt-5-mini"

client = OpenAI(base_url=endpoint, api_key=api_key)

app = Flask(__name__)
CORS(app)

PROMPT = (
    "You are assessing hail damage on a roof from a photo, for an insurance "
    "claims pipeline. Describe what you see, estimate a damage severity tier "
    "from 1 (no damage) to 5 (severe damage / total loss), and briefly justify "
    "the tier in one or two sentences."
)


def assess_roof_bytes(image_bytes):
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model=deployment_name,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": PROMPT},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    },
                ],
            }
        ],
    )

    return response.output_text


@app.route("/assess", methods=["POST"])
def assess():
    if "photo" not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400

    photo = request.files["photo"]
    image_bytes = photo.read()

    if not image_bytes:
        return jsonify({"error": "Empty file"}), 400

    try:
        result = assess_roof_bytes(image_bytes)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"result": result})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
