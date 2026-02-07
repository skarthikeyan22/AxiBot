# 🤖 AxiBot - Local AI YouTube Moderator

AxiBot is a smart, privacy-focused YouTube Live Chat bot powered by **Local AI** (Google Gemma 2 via Ollama). It moderates chat, welcomes subscribers, and replies to viewers just like a human moderator—all without expensive API costs.

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![Local AI](https://img.shields.io/badge/AI-Ollama-orange.svg)

## ✨ Features

- **🧠 Local Intelligence**: Runs locally using **Gemma 2 (2B)**. No API bills, no rate limits.
- **🛡️ Auto-Moderation**: Instantly deletes abusive messages and timeouts users (5 mins).
- **🚫 Anti-Spam**: Enforces a 60-second cooldown per user to prevent flooding.
- **👀 Context Aware**: Knows your current **Stream Title** and **Game**, so it replies relevantly.
- **🤖 Smart Replies**: Casual, human-like responses with minimal emoji usage.
- **⛔ Nightbot Ignore**: Automatically ignores other bots like Nightbot.

---

## 🛠️ Prerequisites

1.  **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
2.  **Ollama**: Required for running the AI model. [Download Here](https://ollama.com/download)

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

3.  **Setup Local AI (Ollama)**
    - Install Ollama from the link above.
    - Open your terminal and run:
      ```powershell
      ollama pull gemma2:2b
      ```
    - Keep Ollama running in the background (`ollama serve`).

---

## 🔑 Configuration (.env)

1.  **Create `.env` file**
    Copy the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Get YouTube Credenitals**
    - Go to **[Google Cloud Console](https://console.cloud.google.com/)**.
    - Create a New Project.
    - Enable **YouTube Data API v3**.
    - Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
    - Choose **Desktop App**.
    - Download the JSON file, rename it to `client_secret.json`, and place it in the project folder.

3.  **Find Your Channel ID**
    - Go to **[YouTube Advanced Settings](https://www.youtube.com/account_advanced)**.
    - Copy the **Channel ID** (starts with `UC...`).

4.  **Edit `.env`**
    Open `.env` and fill in the details:
    ```ini
    # File name of the JSON you downloaded
    YOUTUBE_CLIENT_SECRET_PATH=client_secret.json
    
    # Storage for the login token (auto-created)
    YOUTUBE_TOKEN_PATH=storage/token.json
    
    # YOUR Channel ID (The Streamer)
    STREAMER_CHANNEL_ID=UCxxxxxxxxxxxxxxxxx
    
    # Bot Name (Used to ignore self-replies)
    BOT_NAME=AxiBot
    ```

---

## 🚀 How to Run

1.  **Start the Bot**
    ```powershell
    python -m app.main
    ```

2.  **First Time Login**
    - A browser window will open asking you to log in to Google.
    - Log in with the **account you want the bot to speak from** (usually your main account or a dedicated bot brand account).
    - Determine "unsafe app" warning? Click **Advanced -> Go to (Project Name) (unsafe)**. This happens because your app is in testing mode.
    - Click **Allow**.

3.  **Connection**
    - The console will say: `Connected to Live Chat ID: ...`
    - It will print the **Stream Title** it detected.
    - The bot is now live!

---

## 📝 Customization

- **Bad Words**: Edit `app/moderation_filter.py` to add/remove banned words.
- **Cooldown**: Edit `app/router.py` (change `COOLDOWN_SECONDS`).
- **AI Prompt**: Edit `app/local_client.py` to change how the bot speaks.

---

## ❓ Troubleshooting

- **"Quota Exceeded"**: The bot polls chat every 20 seconds. This allows for ~6 hours of runtime per day on the free tier.
- **"Ollama Connection Error"**: Make sure Ollama is running (`ollama serve`).
- **Bot replying to itself**: Ensure `BOT_NAME` in `.env` matches the bot's display name exactly.
