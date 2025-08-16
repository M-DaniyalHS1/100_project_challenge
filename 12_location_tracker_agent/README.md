# 🌍 GeoLocation Agent

## A conversational AI assistant that returns geolocation information of any IP address using the OpenAI Agent SDK, OpenRouter LLM, and Chainlit UI.

Ask it:

"Where is 8.8.8.8 located?"
"Tell me the city of IP 103.129.234.23"

🚀 Features
✅ Fetches real-time geolocation for public IPs
✅ Structured markdown output with location, city, country, org
✅ Built-in dataclass formatting with emojis
✅ Chainlit UI for real-time interaction
✅ Gracefully handles private IPs and invalid lookups

🧠 Tech Stack
Tech	Purpose
🧠 OpenAI Agent SDK	Agent tools + reasoning engine
🔗 Chainlit	Chat frontend for LLMs
🌐 ipapi.co	IP to location API
🤖 OpenRouter	LLM backend (Mistral model used)
🐍 Python	Core logic and agent orchestration

📦 Setup Instructions
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/M-DaniyalHS1/100_project_challenge/tree/master/12_location_tracker_agent
cd geolocation-agent
2. Create .env file
env
Copy
Edit
ROUTER_API_KEY=sk-or-your-api-key-here
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
If you don’t have a requirements.txt, here's the minimal:

bash
Copy
Edit
pip install chainlit requests python-dotenv
4. Run the agent
bash
Copy
Edit
chainlit run main.py -w
Then open http://localhost:8000 in your browser.

🧪 Example IPs to Try
8.8.8.8 → Google DNS

1.1.1.1 → Cloudflare

103.129.234.23 → Pakistani IP

192.168.1.100 → Private IP (shows fallback)

🛡 Private IP Handling
Private IPs like 192.168.x.x, 10.x.x.x, etc., are not geolocatable — the agent detects this and responds with a meaningful message.

📌 Future Improvements
🌐 Add Google Maps link

🔍 Reverse IP lookup (get hostname)

🧭 Combine with weather or timezone APIs

🌍 Auto-detect user’s current public IP

🤝 Contributing
Pull requests are welcome! Fork the repo and open a PR with your improvements or ideas.

📄 License
MIT License © [Your Name]

🙏 Acknowledgements
Chainlit — UI for AI agents

OpenRouter — LLM provider

ipapi.co — Free IP geolocation API

OpenAI Agent SDK — Agent tools engine
