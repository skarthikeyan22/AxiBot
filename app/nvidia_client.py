from openai import AsyncOpenAI
import random
from app.settings import settings

class NvidiaClient:
    def __init__(self, model_name=None):
        self.model_name = model_name or settings.NVIDIA_MODEL_ID
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=settings.NVIDIA_API_KEY
        )
        self.stream_context = {}
        self.fallback_messages = [
            "I'm overloaded right now! 😵",
            "Too many messages! Give me a second... 🕒",
            "Thinking... (API Rate Limit)",
            "🤖 *beeping noises*",
            "Need to recharge! 🔋"
        ]
        print(f"initialized NvidiaClient with model: {self.model_name}")

    async def generate_reply(self, user: str, message: str, history: str = "", is_mentioned: bool = False) -> str:
        """
        Generates a friendly, short reply.
        Handles context-aware dynamic jumping into chat.
        """
        context_str = ""
        if self.stream_context:
            title = self.stream_context.get("title", "Unknown Stream")
            channel = self.stream_context.get("channel_title", "Unknown Channel")
            context_str = f"You are watching the stream '{title}' on channel '{channel}'. "

        intervention_rules = (
            "You MUST reply. " if is_mentioned else 
            "Read the chat history. If the user is asking a question or genuinely needs help, reply. Otherwise, if they are just chatting generally, strictly output exactly the text: IGNORE_CHAT"
        )

        prompt = (
            f"You are {settings.BOT_NAME}, an empathetic, friendly, human-like YouTube live stream moderator. "
            f"{context_str}\n"
            "CRITICAL RULES:\n"
            "1. Detect the user's language (Tamil, Tanglish, English, etc.) and reply in the EXACT SAME language and modulation.\n"
            "2. Catch their emotions. Be friendly, helpful, and natural. Limit emojis to max 1.\n"
            "3. Keep replies very short (under 200 characters). Do not use URLs.\n"
            f"4. {intervention_rules}\n"
            "---\n"
            f"Recent Chat History:\n{history}\n"
            "---\n"
            f"Latest Message from '{user}': '{message}'\n"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            if response.choices and response.choices[0].message.content:
                reply = response.choices[0].message.content.strip()
                return reply
            return None
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "403" in error_str:
                print(f"Nvidia API Rate Limit Hit: {e}")
                return random.choice(self.fallback_messages)
            
            print(f"Nvidia API Error: {e}")
            return None


    async def generate_engagement_message(self, category: str) -> str:
        """
        Generates a short, engaging message based on the category.
        """
        prompts = {
            "like_subscribe": "Generate a short, fun message asking viewers to like the stream and subscribe to the channel. Be creative! Max 1 emoji.",
            "likes_target": "Generate a short message setting a small likes goal (e.g., 10 or 20 likes) for the stream. Be encouraging! Max 1 emoji.",
            "chat_with_me": "Generate a short message inviting viewers to chat with you (the bot). Ask them a simple question or just say you're ready to chat. Max 1 emoji.",
            "welcome": "Generate a short, warm welcome message for new viewers joining the stream. Max 1 emoji.",
            "like_target_met": "We hit the like goal! 🎉 Generate a short celebration message and set a new higher goal. Max 1 emoji.",
            "sub_target_met": "We hit the subscriber goal! 🚀 Generate a short celebration message for the new subscriber and mention the next goal. Max 1 emoji."
        }
        
        base_prompt = prompts.get(category, prompts["like_subscribe"])
        
        full_prompt = (
            f"You are {settings.BOT_NAME}, a friendly YouTube moderator. "
            f"{base_prompt} "
            "Keep it under 100 characters. No URLs. Do not repeat typical phrases exactly."
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.8,
                max_tokens=60
            )
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip().replace('"', '')
            return None
        except Exception as e:
            # print(f"Nvidia Engagement Error: {e}")
            return None


if __name__ == "__main__":
    import asyncio
    
    async def test():
        print("Testing Nvidia Client...")
        client = NvidiaClient()
        reply = await client.generate_reply("TestUser", "Hello bot! How are you doing?")
        print(f"Reply: {reply}")
        
        engagement = await client.generate_engagement_message("chat_with_me")
        print(f"Engagement: {engagement}")
    
    try:
        asyncio.run(test())
    except KeyboardInterrupt:
        print("Stopped.")
