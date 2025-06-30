import asyncio
import os
from dotenv import load_dotenv
import requests
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    function_tool,
    set_tracing_disabled,
    Agent,
    Runner,
)
from openai.types.responses import ResponseTextDeltaEvent
from typing import List
from agents.repl import run_demo_loop
from pydantic import BaseModel, Field
from dataclasses import dataclass
from lengthy import agent_instructions
import chainlit as cl

# Load .env variables
load_dotenv()
set_tracing_disabled(disabled=True)

# Load router key
router_api_key = os.getenv("ROUTER_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")
if not router_api_key and not newsapi_key:
    raise ValueError("api key error: configure your api keys in the .env file")

# Set provider and model
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

provider = AsyncOpenAI(api_key=router_api_key, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=provider)

# 📰 News Article DataClass with __str__ method for pretty output
@dataclass
class NewsArticle:
    source: str
    title: str
    description: str
    url: str
    published_at: str

    def __str__(self):
        return f"""### 📰 {self.title}
**Source:** {self.source}  
**Published:** {self.published_at}  

**Description**: {self.description or "_No description available._"}

👉 [Read Full Article] ({self.url})
"""

# 🔧 Tool to fetch news
@function_tool
async def get_news(topic: str = "technology", country: str = "pk") -> List[NewsArticle]:
    """
    Fetches the latest news headlines based on a given topic and country.
    """
    url = f"https://newsapi.org/v2/top-headlines?country={country}&q={topic}&apiKey={newsapi_key}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching news: {response.status_code} - {response.text}")

    data = response.json()
    articles = data.get("articles", [])
    print(f"\nTotal articles fetched: {len(articles)}\n\n")

    return [
        NewsArticle(
            source=article["source"]["name"],
            title=article["title"],
            description=article["description"],
            url=article["url"],
            published_at=article["publishedAt"]
        )
        for article in articles[:3]
    ]

# 🧠 Create the NewsAgent
news_agent = Agent(
    name="NewsAgent",
    instructions=agent_instructions,
    model=model,
    tools=[get_news],
    output_type=List[NewsArticle],
    tool_use_behavior="required",
)

# 🎉 On chat start: greet the user
@cl.on_chat_start
async def starter():
    cl.user_session.set("history", [])
    cl.user_session.set("agent", news_agent)

    await cl.Message(
        
    content="👋 Welcome to the 📰 News Agent! Ask me for the latest news on any topic or country 🌍."
).send()



# 💬 Handle user input and show nicely formatted news
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})
    cl.user_session.set("history", history)

    agent = cl.user_session.get("agent", news_agent)
    result = await Runner.run(agent, input=message.content)
    output = result.final_output

    if isinstance(output, list) and all(isinstance(a, NewsArticle) for a in output):
        for article in output:
            msg = cl.Message(content="")  # Placeholder
            await msg.send()  # Initialize the message
            for line in str(article).splitlines():
                await msg.stream_token(line + "\n")
            await msg.update()  # Finalize it
    elif isinstance(output, NewsArticle):
        msg = cl.Message(content="")
        await msg.send()
        for line in str(output).splitlines():
            await msg.stream_token(line + "\n")
        await msg.update()
    else:
        await cl.Message(content="❌ No articles found. Try another topic or country.").send()

    history.append({"role": "assistant", "content": str(output)})
    cl.user_session.set("history", history)
