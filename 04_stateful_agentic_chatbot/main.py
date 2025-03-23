# Import required libraries
import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure the API provider (Gemini) using OpenAI-compatible endpoint
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Configure the language model settings
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Create an AI agent instance with a name and instructions
agent1: Agent = Agent(
    name="Dani",
    instructions="You are a helpul assistant that answers users questions."
)

# Set up the configuration for running the agent
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# Test run with a sample question (synchronous)
result = Runner.run_sync(
    input="What is the capital of france?",
    run_config=run_config,
    starting_agent=agent1
)

# Chainlit chat interface handlers

@cl.on_chat_start
async def handle_chat_start():
    """
    Initialize chat session when a new user connects
    Creates an empty history list and sends a welcome message
    """
    cl.user_session.set("history", [])
    await cl.Message(content="Assalamo-a-Alaikum! My name is Dani 🤖✨ How may I assist you today? 😊🌟").send()

@cl.on_message
async def handle_message(message: cl.Message):
    """
    Handle incoming user messages
    - Maintains conversation history
    - Processes message through the AI agent
    - Updates history with response
    - Sends response back to user
    """
    # Get current chat history
    history = cl.user_session.get("history")
    
    # Add user message to history
    history.append({"role": "user", "content": message.content})
    
    # Process message through AI agent
    result = await Runner.run(
        starting_agent=agent1,
        input=history,
        run_config=run_config,
    )
    
    # Add AI response to history
    history.append({"role": "assistant", "content": result.final_output})
    
    # Update session history and send response
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()