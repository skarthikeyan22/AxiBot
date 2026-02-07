import asyncio
import time
from app.settings import settings
from app.moderation_filter import ModerationFilter

class MessageRouter:
    def __init__(self, gemini_client=None, youtube_client=None):
        self.gemini_client = gemini_client
        self.youtube_client = youtube_client
        self.bot_name = settings.BOT_NAME.lower()
        self.cooldowns = {}
        self.COOLDOWN_SECONDS = 60



    async def route_message(self, message_data: dict):
        """
        Parses raw event data and routes it if it's a valid chat message.
        """
        # Debug: Print ALL events to see structure
        # print(f"[Router Debug] Processing: {message_data}")

        # Handling Streamlabs 'event' structure
        if not isinstance(message_data, dict):
            return

        user_id = None
        message_id = None

        # Standardized Internal Format (Native Listener)
        if message_data.get('platform') == 'youtube' and message_data.get('type') == 'chat':
            user = message_data.get('user')
            message = message_data.get('message')
            user_id = message_data.get('user_id')
            message_id = message_data.get('id')
            # Fall through to processing
        else:

            # Legacy/Streamlabs Handling
            event_type = message_data.get('type')
            
            # 1. Alert Handling (Follow/Subscription)
            if event_type in ['follow', 'subscription', 'resub']:
                # The data structure varies, but usually 'name' or 'message' contains the user
                # Streamlabs often sends: { 'type': 'follow', 'message': [{'name': 'User', ...}] }
                # OR a flat object. We try to extract safely.
                name = message_data.get('name')
                
                # Check if message is a list of events
                raw_msg = message_data.get('message')
                if isinstance(raw_msg, list) and len(raw_msg) > 0:
                    name = raw_msg[0].get('name')
                elif isinstance(raw_msg, dict):
                    name = raw_msg.get('name')
                
                if name:
                    print(f"New Alert: {event_type} from {name}")
                    if self.gemini_client:
                        # Generate a custom welcome message
                        prompt = (
                            f"Generate a very short, enthusiastic thank you message for '{name}' who just subscribed to the channel. "
                            f"You are {self.bot_name}. No URLs."
                        )
                        reply = await self.gemini_client.generate_reply(name, prompt) # overload or use new method?
                        # Actually generate_reply takes (user, message). Use message as the prompt context or overload?
                        # Let's direct call client or just pass the prompt as the 'message' effectively.
                        # Wait, generate_reply assumes "The viewer said: {message}". 
                        # We should add a specific method or just hack it. 
                        # Hack: Pass a special flag or just use the prompt.
                        # For now, let's use the underlying client directly or modify generate_reply.
                        # Easiest: Just use the client model directly here or add helper.
                        
                        # Let's add a helper in GeminiClient? Or just reuse generate_content from here if we had access?
                        # We can abuse generate_reply by saying "I just subscribed!" as the message.
                        reply = await self.gemini_client.generate_reply(name, "I just subscribed to the channel!")
                        
                        if reply and self.youtube_client:
                            self.youtube_client.send_message(reply)
                return

            # Normal Streamlabs Chat (Fallback)
            print(f"[Streamlabs Event] Type: {event_type} | Data: {message_data}")
            user = message_data.get('from') or message_data.get('user') or message_data.get('name')
            message = message_data.get('message') or message_data.get('body') or message_data.get('text')

        if not user or not message or not isinstance(message, str):
            # If we haven't extracted user/message properly yet
            return

        # 0. Self-Reply Prevention
        # Ignore messages from the bot itself
        # Debug: Check exact values
        if user:
            # check for partial match too?
            if user.lower() == self.bot_name or self.bot_name in user.lower() or "nightbot" in user.lower():
                print(f"[Router Ignore] Ignored message from {user}")
                return
            # print(f"[Debug] Message from: '{user}' (Bot name: '{self.bot_name}')")

        # 0.5 Moderation Check
        if ModerationFilter.check_message(message):
            print(f"[Moderation] Abusive message detected from {user}: {message}")
            if self.youtube_client:
                if user_id:
                    self.youtube_client.timeout_user(user_id, duration_seconds=300)
                if message_id:
                    self.youtube_client.delete_message(message_id)
            return

        # 1. Mention Detection
        # Check if the message contains the bot name (case-insensitive)
        user_lower = user.lower() if user else ""
        message_lower = message.lower()
        
        print(f"[Router Parse] User: {user}, Message: {message}")
        
        if f"@{self.bot_name}" not in message_lower and self.bot_name not in message_lower:
            print(f"[Router Ignore] Message does not mention @{self.bot_name}")
            return

        print(f"[{user}] mentioned bot: {message}")

        # 2. Cooldown Check
        if self._is_on_cooldown(user):
            print(f"User {user} is on cooldown.")
            return

        # 3. Gemini AI Generation
        if self.gemini_client:
            print("Generating reply...")
            reply = await self.gemini_client.generate_reply(user, message)
            
            if reply:
                print(f"Bot Reply: {reply}")
                # 4. Send to YouTube
                if self.youtube_client:
                    self.youtube_client.send_message(reply)
                else:
                    print("YouTube Client not connected, cannot send reply.")

    def _is_on_cooldown(self, user: str) -> bool:
        now = time.time()
        last_time = self.cooldowns.get(user, 0)
        
        if now - last_time < self.COOLDOWN_SECONDS:
            return True
        
        self.cooldowns[user] = now
        return False
