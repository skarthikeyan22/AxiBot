# 🤖 AxiBot - AI YouTube Moderator

AxiBot is a smart, privacy-focused YouTube Live Chat bot powered by **Nvidia Open-Source Models API** (e.g., Google Gemma 3). It moderates chat, welcomes subscribers, engages viewers, and manages stream goals just like a human moderator—all optimized for minimal YouTube API usage and blazing fast inference.

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![AI API](https://img.shields.io/badge/AI-Nvidia_NIM-green.svg)

## ✨ Features

- **🧠 High-Performance Intelligence**: Uses NVIDIA's API to run top-tier open-source models (like Gemma 3) with extremely low latency.
- **🗣️ Context-Aware & Multi-lingual**: 
    - **Organic Interception**: Maintains a rolling chat history and intelligently decides when to jump in and help viewers without needing to be literally mentioned via `@AxiBot`.
    - **Native Tongue Matching**: Automatically detects the viewer's language (e.g., Tamil, English, Tanglish) and emotional state, replying with perfectly matched modulations and empathy.
- **🎯 Auto-Updating Goals**:
    - **Like Target**: Automatically sets a goal (starts at 10). When hit, it celebrates and sets the next goal (+10).
    - **Subscriber Target**: Tracks your sub count. When you get a new sub (hitting the "Next 10" milestone), it celebrates and updates the target.
- **📣 Smart Engagement**:
    - **Dynamic Hype**: Generates unique, non-repeating "Like & Subscribe" reminders using AI.
    - **Human-like Timing**: Posts messages at random intervals to feel natural.
    - **Spike Detection**: Welcomes new viewers when traffic spikes.
- **🛡️ Auto-Moderation**: Instantly deletes abusive messages and timeouts users (5 mins).
- **🚫 Anti-Spam**: Enforces a 60-second cooldown per user.
- **⚡ Optimized Quota**: Smart polling allows the bot to run for **8.5+ hours** continuously on the free YouTube quota.

---

## 🛠️ Prerequisites

1.  **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
2.  **Nvidia API Key**: [Get Key Here](https://build.nvidia.com/) (Required for AI generation)

---

## 📥 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/axibot.git
    cd axibot
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔑 Configuration (.env)

1.  **Create `.env` file**
    Copy the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Get YouTube Credentials**
    - Go to **[Google Cloud Console](https://console.cloud.google.com/)**.
    - Create a New Project & Enable **YouTube Data API v3**.
    - Create **OAuth client ID** (Desktop App).
    - Download JSON as `client_secret.json`.

3.  **Edit `.env`**
    ```ini
    YOUTUBE_CLIENT_SECRET_PATH=client_secret.json
    YOUTUBE_TOKEN_PATH=storage/token.json
    STREAMER_CHANNEL_ID=UCxxxxxxxxxxxxxxxxx
    BOT_NAME=AxiBot
    NVIDIA_API_KEY=your_nvidia_api_key_here
    NVIDIA_MODEL_ID=google/gemma-3-4b-it
    ```

---

## 🚀 How to Run

1.  **Start the Bot**
    ```powershell
    python app/main.py
    ```

2.  **First Time Login**
    - A browser window will open. Log in with the account you want the bot to speak from.
    - If you see "Unsafe App", click **Advanced -> Go to (Project) -> Allow**.

3.  **You're Live!**
    - The bot will detect your active stream.
    - It will automatically greet viewers and start monitoring chat.

---

## 📝 Customization

- **Bad Words**: Edit `app/moderation_filter.py`.
- **Engagement Settings**: Edit `app/engagement.py` to change message frequency or target increments.
- **AI Personality**: Edit prompt templates in `app/nvidia_client.py`.

---

## ❓ Troubleshooting

- **"Quota Exceeded"**: The bot is optimized for ~8.5 hours. If you stream longer, create a second project/credential.
- **"401 Unauthorized" or API Key Errors**: Ensure your `NVIDIA_API_KEY` is correct in `.env`.
- **Bot replying to itself**: Ensure `BOT_NAME` in `.env` matches the bot's display name exactly.
