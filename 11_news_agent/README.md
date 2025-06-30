## 📰 Real-Time News Agent 🤖

A conversational AI agent that fetches the latest news in real-time using **NewsAPI**, built with **OpenAI Agent SDK**, **Chainlit**, and **OpenRouter LLMs**. Ask about any topic or country and get clean, structured headlines streamed directly in chat.

---

### 🚀 Features

* 🔍 Ask for news on any **topic** or **country**
* 📄 Structured Markdown output (title, source, date, link)
* 🎯 Uses `dataclass` with `__str__` for clean formatting
* ⚡ Simulated streaming for a chat-like experience
* 🧠 Powered by OpenAI’s **Agent SDK** and `function_tool`

---

### 🧠 Tech Stack

| Component           | Purpose                             |
| ------------------- | ----------------------------------- |
| 🧠 OpenAI Agent SDK | Agentic workflow and function tools |
| 🔗 Chainlit         | Chat UI framework for LLMs          |
| 🌍 NewsAPI          | Source for real-time headlines      |
| ⚡ OpenRouter        | LLM provider (Mistral or other)     |
| 🐍 Python           | Language + dataclass/pydantic usage |

---

### 📦 Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/M-DaniyalHS1/news-agent
cd news-agent
```

#### 2. Create `.env` File

```ini
ROUTER_API_KEY=your_openrouter_api_key
NEWSAPI_KEY=your_newsapi_key
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the App

```bash
chainlit run pra_request.py
```

---

### 🧪 Example Prompt

> **"Latest AI news in the US"**
> or
> **"Top sports headlines in Pakistan"**

---

### 📈 Next Goals

* ✅ Real-time LLM-style streaming
* 🛡️ Guardrails for safe topic control
* 🔍 Tracing and visual debugging of the workflow

---

### 🤝 Contributing

Contributions are welcome! If you have ideas for improvements (multi-language support, summarization, UI enhancements), feel free to fork and PR.

---

### 📄 License

MIT License © \[Daniyal]

---

### 🙌 Acknowledgements

* [OpenRouter](https://openrouter.ai)
* [NewsAPI.org](https://newsapi.org)
* [Chainlit](https://www.chainlit.io)
* [OpenAI Agent SDK](https://github.com/openai/openai-agents)

## Results:
    ![News agent in action]("crypto_agent\news_agent.jpg")


