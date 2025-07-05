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
    Runner,ModelSettings,RunContextWrapper
)
from openai.types.responses import ResponseTextDeltaEvent
from typing import List
from agents.repl import run_demo_loop
from pydantic import BaseModel, Field
from dataclasses import dataclass
import chainlit as cl

# Load .env variables
load_dotenv()
set_tracing_disabled(disabled=True)

# Load router key
router_api_key = os.getenv("ROUTER_API_KEY")
if not router_api_key :
    raise ValueError("api key error: configure your api keys in the .env file")

# Set provider and model
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

provider = AsyncOpenAI(api_key=router_api_key, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=provider)

@function_tool
async def price_checker():
    """this function uses the binance api and fetcher the top 10 crypto currence prices and return to agent"""

    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        top_10 = data[:10]
        result = ""
        for coin in top_10:
            result += f"- {coin['symbol']}: ${coin['price']}\n"
        return result
    except Exception as e:
        return f"some thing happened: \n{e}\n"



crypto_agent = Agent(name = "crypto_agent",    instructions="""
You are a cryptocurrency expert AI assistant. 
Your job is to respond to user queries about live crypto prices.
Use tools to:
- Show top 10 crypto prices when the user says things like "top", "show top coins", etc.
- Show price of a specific coin like BTCUSDT when user asks for it.
Always be clear, concise, and avoid unnecessary information.
""",
                     model = model ,
                     model_settings = ModelSettings(tool_choice = "required",max_tokens = 500,include_usage = True),
                     tools = [price_checker],
                     handoff_description = "this is crypto agent tells uses tool to tell about crypto currencies",

                     )

supervisor = Agent(name = "supervisor_agent",
                   instructions = "you are helpful assistant",
                   model = model,
                   handoffs = [crypto_agent],
                   )
async def main():
    @cl.on_chat_start
    async def starter():

        """this function send the   message to the user"""
    
        

        cl.user_session.set("history",[])
        await cl.Message("🌟 Welcome to CryptoTracker Agent 🚀 — Get live crypto prices from Binance instantly! 📈🪙💸.").send()
        


        
    @cl.on_message
    async def message_handler(message:cl.Message):
        """this functions take the user input and process it
        """
        history = cl.user_session.get('history')
        history.append({"role":"user","content":message.content})
        cl.user_session.set("history",history)
         
        msg = cl.Message(content = "")

        result = Runner.run_streamed(supervisor,input = history)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data,"delta"):
               token = event.data.delta
               await msg.stream_token(token)


        history.append({"role":"assistant","content":result.final_output})
        cl.user_session.set("history",history)
        await msg.update()


asyncio.run(main())