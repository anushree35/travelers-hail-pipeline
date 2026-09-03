import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("SUCCESS: Gemini API key was found.")
    print("Key begins with:", api_key[:7])
else:
    print("ERROR: Gemini API key was NOT found.")


if api_key:

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents="Respond with exactly: Gemini is working."
    )

    print(response.text)