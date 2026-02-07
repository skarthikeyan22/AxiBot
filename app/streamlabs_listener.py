import socketio
import asyncio
from app.settings import settings

class StreamlabsListener:
    def __init__(self, callback=None):
        self.token = settings.STREAMLABS_SOCKET_TOKEN
        self.sio = socketio.AsyncClient()
        self.callback = callback
        
        # Register event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('event', self.on_event)
        self.sio.on('connect_error', self.on_connect_error)

    async def on_connect(self):
        print("Connected to Streamlabs Socket API")

    async def on_disconnect(self):
        print("Disconnected from Streamlabs Socket API")

    async def on_connect_error(self, data):
        print(f"Connection Error: {data}")

    async def on_event(self, data):
        # Log RAW data to debug what we receive
        # print(f"[DEBUG RAW] {data}") 
        
        if self.callback:
            await self.callback(data)

    async def connect(self):
        url = f"https://sockets.streamlabs.com?token={self.token}"
        while True:
            try:
                print(f"Connecting to {url.split('?')[0]}...")
                await self.sio.connect(url)
                await self.sio.wait()
            except asyncio.CancelledError:
                print("Connection cancelled.")
                break
            except Exception as e:
                print(f"Streamlabs Loop Error: {e}")
                print("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

if __name__ == "__main__":
    # Test standalone
    async def test_run():
        listener = StreamlabsListener()
        await listener.connect()
    
    try:
        asyncio.run(test_run())
    except KeyboardInterrupt:
        print("Stopped.")
