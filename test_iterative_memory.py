import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.router import MessageRouter
from app.nvidia_client import NvidiaClient

async def test_iterative_memory():
    print("=== Testing Iterative Memory + Tell About Me ===")
    
    # Initialize
    client = NvidiaClient()
    router = MessageRouter(gemini_client=client)
    
    user_id = "test-iterative-user"
    display_name = "Karthik"
    
    # 1. First Batch: Establish baseline (PUBG player)
    print(f"\n1. Sending first 6 messages (Initial Profile)...")
    m1 = ["I love PUBG!", "Playing from Chennai.", "M416 is my fav.", "I'm a pro sniper.", "Stream is lit!", "Hello AxiBot!"]
    for msg in m1:
        await router.route_message({"user": display_name, "user_id": user_id, "message": msg, "type": "chat", "platform": "youtube"})
        await asyncio.sleep(0.5)
    
    await asyncio.sleep(5) # Wait for background summarization
    
    # Check baseline
    user_data = router.db.get_user(user_id)
    print(f"Initial Summary: {user_data['personality_summary']}")
    
    # 2. Second Batch: Add new interests (Music/Cooking)
    print(f"\n2. Sending second 6 messages (Update Profile with Music/Cooking)...")
    m2 = ["I also love listening to AR Rahman.", "Do you like Biryani?", "I am learning to cook.", "Tamil music is the best.", "Just finished dinner.", "AxiBot, you remember my SNIPING?"]
    for msg in m2:
        await router.route_message({"user": display_name, "user_id": user_id, "message": msg, "type": "chat", "platform": "youtube"})
        await asyncio.sleep(0.5)
    
    await asyncio.sleep(5) # Wait for iterative summary
    
    # Check updated memory
    user_data = router.db.get_user(user_id)
    print(f"Updated Summary: {user_data['personality_summary']}")
    
    # 3. Test "Tell About Me"
    print("\n3. Testing 'Tell About Me' prompt...")
    await router.route_message({
        "user": display_name, 
        "user_id": user_id, 
        "message": "AxiBot, tell about me! what do you know?", 
        "type": "chat",
        "platform": "youtube"
    })
    # The output will be printed in the terminal logs from the router.

if __name__ == "__main__":
    asyncio.run(test_iterative_memory())
