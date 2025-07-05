💹 CryptoTracker Agent
🚀 CryptoTracker Agent is an AI-powered assistant that fetches live cryptocurrency prices from the Binance API using natural language queries.
It’s built with Chainlit, OpenAI Agent SDK, and runs on OpenRouter.

🌟 Features
📈 Get real-time prices of top cryptocurrencies

🤖 Ask for top 10 coins or a specific coin price like BTCUSDT

🔌 Fully integrated with Binance API

🧠 Powered by advanced LLMs via OpenRouter

🛠️ Tech Stack
🧠 OpenAI Agent SDK

🗣️ Chainlit (Chat UI)

🌐 Binance Public API

🔑 OpenRouter (LLM gateway)

🐍 Python 3.10+

📦 dotenv, requests, pydantic

⚙️ Setup Instructions
Clone the repository


bash
Copy
Edit
pip install -r requirements.txt
Configure your .env

env
Copy
Edit
ROUTER_API_KEY=your_openrouter_api_key
Run the app

bash
Copy
Edit
chainlit run main.py
💬 Example Prompts
"Show top 10 crypto prices"

"What’s the price of BTCUSDT?"

"Tell me about ETHUSDT"

📸 Preview
🌟 Welcome to CryptoTracker Agent — Get live crypto prices from Binance instantly! 📊🪙💸


🧠 How It Works
A supervisor_agent handles user queries and delegates tasks

A specialized crypto_agent uses tools to call the Binance API

Responses are streamed to the user with token-by-token updates

📜 License
MIT License © 2025 [M.DANIYAL]

