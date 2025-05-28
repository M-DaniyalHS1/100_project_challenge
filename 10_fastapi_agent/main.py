from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,RunConfig,function_tool
from dotenv import load_dotenv
import os
import asyncio
from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from uuid import uuid4
from datetime import timezone as UTC
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import chainlit as cl


app = FastAPI()

set_tracing_disabled(True)

load_dotenv() # Load environment variables from .env file

# Ensure GEMINI_API_KEY is loaded
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please check your .env file.")

external_client = AsyncOpenAI(
    base_url ="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key = gemini_api_key,
)

# Using a more standard Gemini model name. Please verify the exact model name.
model = OpenAIChatCompletionsModel(
    model = "gemini-1.5-flash", # Changed model name, verify this with Google AI documentation
    openai_client = external_client
)

runconfig = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)


web_developer = Agent(
    name = "web developer agent",
    instructions = "You are a web developer expert agent, you create very and creative websites and custom integrations according to users requirement.",
    model=model,
    handoff_description = "web developer expert"
)

mobile_developer = Agent(
    name = "mobile developer agent",
    instructions = "You are a mobile developer expert agent, you create very and creative mobile apps and applications and custom integrations according to users requirement.",
    model=model,
    handoff_description = "mobile developer expert"
)

@function_tool
async def devops():
    """You are a helpful devops agent"""
    # In a real scenario, you would implement devops functionalities here
    pass

@function_tool
async def openai_agent():
    """You are a helpful openai agent"""
    # In a real scenario, you would implement openai agent functionalities here
    pass


agentic_ai = Agent (
    name = "agentic ai expert",
    instructions = "You are a agentic ai expert agent, you create very and creative agentic applications and custom integrations according to users requirement. also you give information about agentic ai in modern world latest trends in agentic ai according to user queries",
    handoff_description = "agentic ai expert",
    model = model,
    tools = [devops,openai_agent]
)


panacloud_agent = Agent(
    name = "panacloud",
    instructions = "You are triage agent you observe user task and delegates tasks to specific agent that is specialized in it.",
    model = model,
    handoffs= [web_developer,mobile_developer,agentic_ai]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    session_id: str = Field(default_factory=lambda: str(uuid4()))


class Response(BaseModel):
    user_id:str
    response:str

class Message(BaseModel):
    user_id: str
    text:str
    user_name:str

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic AI Expert API. Use /start/{user_id} to start a chat."}


@app.get("/start/{user_id}")
async def chat_start(user_id:str,user_name:str,role:str | None = None):
    return {"user_id": user_id,"user_name":user_name}


async def stream_response(message_text: str,user_name:str):
    result = Runner.run_streamed(starting_agent=panacloud_agent, run_config=runconfig, input=message_text)
    async for event in result.stream_events():
        if event.type == 'raw_response_event' and hasattr(event.data, "delta"):
            yield f"data: {user_name}\n\n{event.data.delta}\n\n"
    # Optionally, yield a final message to indicate completion or any summary
    # yield "data: [END]\n\n" # A common way to signal end of stream

@app.post("/chat/stream") # Removed response_model as it's a StreamingResponse
async def chat_stream(message: Message):
    if not message.text.strip():
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    return StreamingResponse(
        stream_response(message.text,user_name=message.user_name),
        media_type="text/event-stream"
    )

@cl.on_chat_start
async def starter():
    print("\n\nDEBUG:************************ Chat started , client connected through api calls.**********************************\n\n")
    await cl.Message(content="Welcome to the Agentic AI Expert! How can I assist you today?").send()

@cl.on_message
async def chats(message:cl.Message):
    # This print statement is KEY for debugging!
    print(f"DEBUG: Received message from client:----------- {message.content}\n\n-----------------")

    if not message.content.strip():
        await cl.Message(content ="Message text cannot be empty").send()
    else:
        # 1. Create the message object
        msg = cl.Message(content='')
        # 2. Send the initial empty message to start streaming
        await msg.send()

        response = Runner.run_streamed(
            starting_agent = panacloud_agent,
            run_config = runconfig,
            input = message.content
        )
        # 3. Stream tokens within the loop
        async for event in response.stream_events():
            if event.type =="raw_response_event" and hasattr(event.data,"delta"):
                await msg.stream_token(event.data.delta)
        
        # 4. ONLY send the message one last time AFTER the loop finishes
        # This finalizes the streamed message.
        await msg.send()
                




