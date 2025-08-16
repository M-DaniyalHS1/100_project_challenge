# 🤖 Agentic AI Expert – Multi-Agent System with FastAPI, Chainlit & OpenAI Agent SDK

Welcome to the **Agentic AI Expert** project! This is a full-stack, multi-agent AI system that uses **FastAPI**, **Chainlit**, and the **OpenAI Agent SDK** (with support for **Gemini 1.5 Flash**) to deliver a real-time, intelligent, and modular chatbot experience 💬⚡

---

## 🚀 Project Highlights

* 🤖 Multiple **expert agents** (Web Dev, Mobile Dev, DevOps, Agentic AI)
* 🎯 A **triage agent** that routes tasks to the appropriate specialized agent
* ⚡ **FastAPI** backend for real-time chat streaming & session handling
* 🧠 Powered by **OpenAI Agent SDK** and **Gemini 1.5 Flash API**
* 💬 **Chainlit** provides an interactive frontend chat interface
* 🔌 Real-time response streaming using `Runner.run_streamed()`

---

## 📁 Project Structure

```
📦 project/
├── main.py              # FastAPI app & Chainlit integration
├── .env                 # Environment variables (e.g., GEMINI_API_KEY)
├── requirements.txt     # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/agentic-ai-expert.git
cd agentic-ai-expert
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory with:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> 🛡️ Your API key will be used to access Gemini 1.5 Flash via OpenAI-compatible routes.

### 4. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 5. Run Chainlit frontend (in another terminal)

```bash
chainlit run main.py
```

---

## 🔌 API Endpoints

| Method | Route              | Description                  |
| ------ | ------------------ | ---------------------------- |
| GET    | `/`                | Welcome route                |
| GET    | `/start/{user_id}` | Start a new chat session     |
| POST   | `/chat/stream`     | Streamed chat endpoint (SSE) |

---

## 🧠 Agents Overview

| Agent Name         | Role & Expertise                                  |
| ------------------ | ------------------------------------------------- |
| `web_developer`    | Builds websites and web integrations              |
| `mobile_developer` | Develops mobile apps and cross-platform solutions |
| `devops`           | Handles infrastructure, CI/CD (stub for now)      |
| `openai_agent`     | Placeholder for general OpenAI tasks              |
| `agentic_ai`       | Expert in agentic AI, trends, and implementations |
| `panacloud_agent`  | Delegates tasks to the right expert agent         |

---

## 🌍 Live Sharing & Testing

Use tools like [ngrok](https://ngrok.com/) to forward your local FastAPI port and test the app with others in real time:

```bash
ngrok http 8000
```

---

## 🧪 Example Use Cases

* Ask for help building a website or mobile app
* Learn about current trends in Agentic AI
* Get DevOps guidance (extend `devops()` for real utility!)
* Experience multi-agent task delegation in action


## 🛠️ Tech Stack

* 🐍 Python 3.10+
* ⚡ FastAPI
* 🤖 OpenAI Agent SDK
* 🌐 Chainlit
* 🔐 Gemini API (OpenAI-compatible)
* 🧪 Uvicorn for local dev server

---

## 🤝 Contributions

Pull requests and feedback are welcome! Feel free to fork the project, improve agent logic, or expand its capabilities.

---

## 📄 License

MIT License

---

## 🙌 Acknowledgements

Special thanks to:

* [OpenAI](https://platform.openai.com/) for the Agent SDK
* [Chainlit](https://www.chainlit.io/) for the amazing UI framework
* [Google's Gemini](https://ai.google.dev/) for powering the intelligence

---

## 📬 Let’s Connect!

If you liked this project or want to collaborate on AI agents, feel free to reach out or ⭐ the repo!
