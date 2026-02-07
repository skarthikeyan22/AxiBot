from google import genai
from app.settings import settings
import asyncio

async def list_models():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    print("Listing models...")
    try:
        # Pager object for list_models
        # In new SDK it might be client.models.list()
        # let's try to iterate
        async for model in await client.aio.models.list():
            print(f"Found model: {model.name}")
            
    except Exception as e:
        print(f"List Error: {e}")
        # Try synchronous
        try:
             for model in client.models.list():
                print(f"Found model (sync): {model.name}")
        except Exception as e2:
             print(f"List Sync Error: {e2}")

if __name__ == "__main__":
    asyncio.run(list_models())
