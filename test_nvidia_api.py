import asyncio
import sys
import os

# Add project root to sys.path so we can import app modules easily
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.nvidia_client import NvidiaClient

async def test_nvidia_api():
    print("\n=== Initializing Nvidia Client Test ===")
    try:
        client = NvidiaClient()
        print(f"Successfully loaded client for model: {client.model_name}")
        
        print("\n--- 1. Testing Chat Completion ---")
        reply = await client.generate_reply("TestUser", "Hello bot! Give me a random fun fact about space.")
        if reply:
            print(f"✅ Bot Output: {reply}")
        else:
            print("❌ Failed to get a reply.")
            
        print("\n--- 2. Testing Engagement Message ---")
        engagement = await client.generate_engagement_message("like_subscribe")
        if engagement:
            print(f"✅ Engagement Output: {engagement}")
        else:
            print("❌ Failed to get an engagement message.")
            
        print("\n=== Test Complete ===")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        print("Please check your .env file and ensure NVIDIA_API_KEY is correctly set.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_nvidia_api())
