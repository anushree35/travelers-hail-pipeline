import base64
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
api_key = os.getenv("AZURE_API_KEY")
deployment_name = "gpt-5-mini"

client = OpenAI(base_url=endpoint, api_key=api_key)

PROMPT = (
    "You are assessing hail damage on a roof from a photo, for an insurance "
    "claims pipeline. Describe what you see, estimate a damage severity tier "
    "from 1 (no damage) to 5 (severe damage / total loss), and briefly justify "
    "the tier in one or two sentences."
)


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def assess_roof_photo(image_path):
    b64_image = encode_image(image_path)

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

    return response.output[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hail_vision.py <path_to_roof_photo>")
        sys.exit(1)

    result = assess_roof_photo(sys.argv[1])
    print(result)
