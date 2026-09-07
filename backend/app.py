import base64
import os
import sys
import tempfile
import time

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

# ---------------------------------------------------------------------
# Kyle's Gemini + physics pathway (a second, independent AI approach).
# Imported defensively: if GEMINI_API_KEY isn't set or the import fails
# for any reason, /assess-gemini reports that clearly instead of taking
# the whole backend down, so the primary Azure Foundry demo never
# breaks because of this second one.
# ---------------------------------------------------------------------
GEMINI_AVAILABLE = False
GEMINI_IMPORT_ERROR = None
try:
    sys.path.insert(
        0, os.path.join(os.path.dirname(__file__), "..", "kyle-physics")
    )
    from ai import analyze_image
    from physics import calculate_hail_physics
    from probability import damage_probability
    from reports import classify_damage
    from materials import materials as roof_materials

    GEMINI_AVAILABLE = True
except Exception as exc:
    GEMINI_IMPORT_ERROR = str(exc)

# Roof age, slope, temperature, and impact count aren't visible in a
# single top-down photo, so this quick demo uses reasonable placeholder
# averages for them. A real deployment would pull these from property
# records instead of guessing.
DEFAULT_ENV_INPUTS = {
    "material_age": 10,
    "roof_slope": 6,
    "temperature": 70,
    "num_impacts": 20,
}


def analyze_image_with_retry(image_path, attempts=2, delay_seconds=1.5):
    """Gemini occasionally returns a transient 503 'model overloaded'
    error under high demand, worth one quick retry. A 429 quota/rate
    limit error is NOT worth retrying, the free tier caps this model
    at 20 requests/day, so retrying a quota failure just burns another
    one of a very scarce budget for no chance of success."""
    last_exc = None
    for attempt in range(attempts):
        try:
            return analyze_image(image_path)
        except Exception as exc:
            last_exc = exc
            lowered = str(exc).lower()
            if "resource_exhausted" in lowered or "quota" in lowered or "429" in lowered:
                raise
            if attempt < attempts - 1:
                time.sleep(delay_seconds)
    raise last_exc


def friendly_gemini_error(exc):
    text = str(exc)
    lowered = text.lower()
    if "unavailable" in lowered or "overloaded" in lowered or "high demand" in lowered:
        return "The Gemini API is temporarily overloaded on Google's end, not a bug here. Give it a few seconds and try again."
    if "resource_exhausted" in lowered or "quota" in lowered or "rate limit" in lowered:
        return "The Gemini API's free-tier daily quota for this model has been used up for now. Use the example result below instead, or try again after the quota resets."
    return text

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


@app.route("/assess-gemini", methods=["POST"])
def assess_gemini():
    if not GEMINI_AVAILABLE:
        return (
            jsonify(
                {
                    "error": "Gemini pathway isn't configured on this "
                    f"server: {GEMINI_IMPORT_ERROR}"
                }
            ),
            503,
        )

    if "photo" not in request.files:
        return jsonify({"error": "No photo uploaded"}), 400

    photo = request.files["photo"]
    image_bytes = photo.read()

    if not image_bytes:
        return jsonify({"error": "Empty file"}), 400

    suffix = os.path.splitext(photo.filename or "")[1] or ".jpg"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        features = analyze_image_with_retry(tmp_path)

        inputs = {
            **DEFAULT_ENV_INPUTS,
            "dent_shape": features["dent_shape"],
            "damage_distribution": features["damage_distribution"],
            "dent_depth": features["dent_depth"],
            "dent_diameter": features["dent_diameter"],
        }

        material_data = roof_materials[features["material"]]
        physics = calculate_hail_physics(features["estimated_hail_size"])
        probability = damage_probability(inputs, physics["energy"], material_data)
        risk_level = classify_damage(probability)

        result = {
            "material": features["material"],
            "estimated_hail_size": features["estimated_hail_size"],
            "dent_shape": features["dent_shape"],
            "damage_distribution": features["damage_distribution"],
            "ai_confidence": features["confidence"],
            "analysis_summary": features["analysis_summary"],
            "impact_energy": physics["energy"],
            "damage_probability": probability,
            "risk_level": risk_level,
        }
    except Exception as exc:
        return jsonify({"error": friendly_gemini_error(exc)}), 502
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", debug=debug_mode, port=port)
