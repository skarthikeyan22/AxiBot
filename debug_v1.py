from google import genai
from app.settings import settings
import asyncio

async def test_v1():
    print("Testing Gemini 1.5 Flash with v1...")
    # Try forcing v1alpha or v1beta or v1
    # The SDK docs are sparse, but let's try http_options or similar if we can guess.
    # Actually, the Client usually takes `http_options`
    
    try:
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options={'api_version': 'v1'} 
        )
        
        # List models to see if 1.5 appears
        print("Listing models with v1...")
        async for model in await client.aio.models.list():
            if "1.5" in model.name:
                print(f"Found: {model.name}")
        
        # Try generating
        print("Generating with gemini-1.5-flash...")
        response = await client.aio.models.generate_content(
            model='gemini-1.5-flash',
            contents='Hello'
        )
        print(f"Success: {response.text}")
        
    except Exception as e:
        print(f"Error v1: {e}")

if __name__ == "__main__":
    asyncio.run(test_v1())
