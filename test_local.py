import asyncio
from app.local_client import LocalGemmaClient

async def test_local():
    print("Testing Local Gemma Client...")
    client = LocalGemmaClient(model_name="gemma2:2b")
    reply = await client.generate_reply("TestUser", "Hello bot, are you running locally?")
    print(f"Reply: {reply}")

if __name__ == "__main__":
    asyncio.run(test_local())
