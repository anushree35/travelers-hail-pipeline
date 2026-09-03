import base64
import json
import mimetypes
import os

from dotenv import load_dotenv
from google import genai

from materials import materials


# ---------------------------------------------------------
# Load the Gemini API key from .env
# ---------------------------------------------------------

project_folder = os.path.dirname(
    os.path.abspath(__file__)
)

env_file = os.path.join(
    project_folder,
    ".env"
)

load_dotenv(env_file)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Make sure your .env file exists in the same folder "
        "as main.py and contains GEMINI_API_KEY=your_key_here"
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# Convert the image into data Gemini can receive
# ---------------------------------------------------------

def encode_image(image_path):
    """
    Reads the image and converts it to base64.
    """

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif"
    ]:
        raise ValueError(
            "Unsupported image type. "
            "Please use JPG, JPEG, PNG, WEBP, or GIF."
        )

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return encoded_image, mime_type


# ---------------------------------------------------------
# Analyze the image with Gemini
# ---------------------------------------------------------

def analyze_image(image_path):
    """
    Sends a hail-damage image to Gemini and returns
    the visual features needed by the engineering model.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    print("\nAnalyzing image with Gemini AI...")
    print("Please wait...\n")


    # Read image
    image_data, mime_type = encode_image(image_path)


    # Get material names from our existing database
    material_names = list(materials.keys())

    material_list = "\n".join(
        f"- {material}"
        for material in material_names
    )


    # -----------------------------------------------------
    # AI instructions
    # -----------------------------------------------------

    prompt = f"""
You are an engineering inspection assistant specializing
in hail damage to roofing materials.

Analyze the uploaded image carefully.

Your job is to identify visual evidence of hail damage and
estimate the physical characteristics needed by an
engineering hail-damage model.

AVAILABLE ROOF MATERIALS:

{material_list}

Choose the single material that appears most likely
from the image.

IMPORTANT RULES:

1. Do not invent visual evidence that is not present.

2. If a measurement cannot be known exactly from the
   photograph, provide a reasonable engineering estimate.

3. A photograph normally cannot determine exact hail size
   or exact dent depth without a known scale.

4. Treat dent depth, dent diameter, and hail size as
   ESTIMATES rather than exact measurements.

5. Look for:
   - dents
   - bruises
   - cracks
   - fractures
   - punctures
   - deformation
   - other visible impact damage

6. Determine whether the visible damage appears:
   - circular
   - irregular
   - another recognizable shape

7. Determine whether damage appears:
   - random
   - linear
   - clustered
   - another recognizable pattern

8. Estimate dent diameter in inches.

9. Estimate dent depth in inches.

10. Estimate likely hail diameter in inches.

11. Give a confidence value from 0 to 1.

12. If the image does not provide enough evidence for
    something, make a cautious estimate and explain the
    uncertainty in the analysis summary.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "material": "one material from the available list",
    "dent_shape": "Circular, Irregular, or Other",
    "damage_distribution": "Random, Linear, Clustered, or Other",
    "dent_depth": number,
    "dent_diameter": number,
    "estimated_hail_size": number,
    "confidence": number,
    "analysis_summary": "short explanation of what was observed"
}}

Do not include markdown.

Do not include ```json.

Do not include any text outside the JSON.
"""


    # -----------------------------------------------------
    # Send image + instructions to Gemini
    # -----------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            },
            prompt
        ]
    )


    # Get Gemini's text response
    result_text = response.text.strip()


    # -----------------------------------------------------
    # Convert Gemini's JSON response into Python data
    # -----------------------------------------------------

    try:

        features = json.loads(result_text)

    except json.JSONDecodeError:

        raise ValueError(
            "Gemini returned an unexpected response:\n"
            + result_text
        )


    # -----------------------------------------------------
    # Validate the material
    # -----------------------------------------------------

    if features["material"] not in materials:

        raise ValueError(
            f"Gemini selected an unsupported material: "
            f"{features['material']}"
        )


    # -----------------------------------------------------
    # Display the AI results
    # -----------------------------------------------------

    print("Gemini analysis complete.")
    print()

    print("========== AI IMAGE ANALYSIS ==========")

    print(
        f"Material: "
        f"{features['material']}"
    )

    print(
        f"Dent Shape: "
        f"{features['dent_shape']}"
    )

    print(
        f"Damage Distribution: "
        f"{features['damage_distribution']}"
    )

    print(
        f"Estimated Dent Depth: "
        f"{features['dent_depth']:.3f} in"
    )

    print(
        f"Estimated Dent Diameter: "
        f"{features['dent_diameter']:.2f} in"
    )

    print(
        f"Estimated Hail Size: "
        f"{features['estimated_hail_size']:.2f} in"
    )

    print(
        f"AI Confidence: "
        f"{features['confidence']:.2f}"
    )

    print()

    print("AI Summary:")
    print(features["analysis_summary"])

    print(
        "========================================"
    )

    print()


    return features