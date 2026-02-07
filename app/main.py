import asyncio
import sys
from app.settings import settings
from app.streamlabs_listener import StreamlabsListener
from app.youtube_client import YouTubeClient
from app.gemini_client import GeminiClient
from app.router import MessageRouter

async def main():
    print(f"=== Starting {settings.BOT_NAME} ===")
    
    # 1. Initialize Clients
    print("Initializing clients...")
    # gemini = GeminiClient()
    from app.local_client import LocalGemmaClient
    gemini = LocalGemmaClient(model_name="gemma2:2b")
    
    youtube = YouTubeClient()
    
    # 2. Find Active Live Chat
    # We need to find the chat ID before we start listening, 
    # so we know where to post replies.
    if settings.STREAMER_CHANNEL_ID:
        print(f"Auto-detecting live stream for channel: {settings.STREAMER_CHANNEL_ID}")
        chat_id = youtube.get_live_chat_id_for_channel(settings.STREAMER_CHANNEL_ID)
        if chat_id:
            print(f"Connected to Live Chat ID: {chat_id}")
            youtube.send_message("Hey Viewers Now Iam active you can chat with me by mentioning me...")
            
            # Fetch Stream Context for AI
            if youtube.video_id:
                details = youtube.get_video_details(youtube.video_id)
                if details:
                    print(f"Stream Context: {details.get('title')} | Channel: {details.get('channel_title')}")
                    # Update the AI client with this context
                    if hasattr(gemini, 'stream_context'):
                        gemini.stream_context = details
        else:
            print("WARNING: No active live stream found. The bot will NOT be able to reply.")
            # We continue anyway, maybe they just want to test reading?
            # Or maybe we should retry periodically? For MVP, we warn.
    else:
        print("ERROR: STREAMER_CHANNEL_ID not set in .env")
        return

    # 3. Setup Router with clients
    router = MessageRouter(gemini_client=gemini, youtube_client=youtube)

    # 4. Setup Listeners
    async def on_event(event_data):
        await router.route_message(event_data)

    sl_listener = StreamlabsListener(callback=on_event)
    
    # Import locally to avoid circular imports if any, or just for clarity
    from app.youtube_listener import YouTubeChatListener
    yt_listener = YouTubeChatListener(youtube_client=youtube, callback=on_event)

    # 5. Start Event Loops
    print("Starting Listeners (Streamlabs + Native YouTube)...")
    try:
        # Run both listeners concurrently
        await asyncio.gather(
            sl_listener.connect(),
            yt_listener.start()
        )
    except asyncio.CancelledError:
        print("Bot stopping...")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Interrupted.")
