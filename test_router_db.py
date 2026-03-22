import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.router import MessageRouter
from app.nvidia_client import NvidiaClient

async def test_db_logic():
    print("=== Testing Router + Database Logic ===")
    
    # Initialize
    client = NvidiaClient()
    router = MessageRouter(gemini_client=client)
    
    user_id = "test-user-123"
    display_name = "Abhi"
    
    print(f"\n1. Sending 6 messages from {display_name} to trigger summarization...")
    messages = [
        "Hey! I love PUBG mobile.",
        "I usually play every night.",
        "My favorite weapon is the M416.",
        "I'm from Tamil Nadu!",
        "Can you help me with some tips?",
        "I really like this stream!"
    ]
    
    for msg in messages:
        message_data = {
            "platform": "youtube",
            "type": "chat",
            "user": display_name,
            "user_id": user_id,
            "message": msg,
            "id": "msg-1"
        }
        await router.route_message(message_data)
        # Add a tiny sleep to allow the AI call to finish if synchronous, 
        # though router is async.
        await asyncio.sleep(1)

    print("\n2. Waiting a moment for background summarization...")
    await asyncio.sleep(5)
    
    print("\n3. Verifying database entry...")
    user_data = router.db.get_user(user_id)
    if user_data:
        print(f"User: {user_data['display_name']}")
        print(f"Messages Count: {user_data['message_count']}")
        print(f"Personality Summary: {user_data['personality_summary']}")
    else:
        print("Error: User not found in DB!")

if __name__ == "__main__":
    asyncio.run(test_db_logic())
