from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    STREAMLABS_SOCKET_TOKEN: str
    YOUTUBE_CLIENT_SECRET_PATH: str = "client_secret.json"
    YOUTUBE_TOKEN_PATH: str = "storage/token.json"
    STREAMER_CHANNEL_ID: str # Channel ID of the streamer to watch
    GEMINI_API_KEY: str
    BOT_NAME: str = "AxiBot"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
