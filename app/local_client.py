import aiohttp
import json
from app.settings import settings

class LocalGemmaClient:
    def __init__(self, model_name="gemma2:2b", stream_context=None):
        self.api_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
        self.stream_context = stream_context or {}
        print(f"initialized LocalGemmaClient with model: {self.model_name}")

    async def generate_reply(self, user: str, message: str) -> str:
        """
        Generates a reply using the local Ollama instance.
        """
        context_str = ""
        if self.stream_context:
            title = self.stream_context.get("title", "Unknown Stream")
            channel = self.stream_context.get("channel_title", "Unknown Channel")
            context_str = f"You are watching the stream '{title}' on channel '{channel}'. "

        prompt = (
            f"You are {settings.BOT_NAME}, a friendly human-like moderator. "
            f"{context_str}"
            "Answer the viewer casually. "
            "IMPORTANT: Limit emojis to max 1. Do not reuse the same emoji. "
            "Keep replies short (under 200 chars). No URLs. "
            f"The viewer '{user}' said: '{message}'"
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        reply = data.get("response", "").strip()
                        return reply
                    else:
                        print(f"Ollama API Error: {response.status} - {await response.text()}")
                        return None
        except Exception as e:
            print(f"Local Gemma Connection Error: {e}")
            print("Make sure Ollama is installed and running: 'ollama serve'")
            return None
