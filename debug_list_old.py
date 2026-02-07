import google.generativeai as genai
from app.settings import settings
import asyncio

def list_models_old_sdk():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    print("Listing models (Old SDK)...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}")
    except Exception as e:
        print(f"List Error: {e}")

if __name__ == "__main__":
    list_models_old_sdk()
