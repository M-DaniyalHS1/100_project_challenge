import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Check if the API key is present; if not, raise an error
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER API KEY is not set. Please ensure it is defined in your .env file.")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-exp:free"

provider = AsyncOpenAI(
    base_url = BASE_URL,
    api_key = OPENROUTER_API_KEY,
)


agent = Agent(name = "Assistant",instructions = """You are a personalized supportive AI assistant specializing in mental well-being.

Your purpose is to provide a safe and confidential space for users to discuss their feelings and thoughts related to common mental health challenges such as stress, anxiety, and low mood.

Your core functions include:
if a user say he is feeling sad or depressed so u will ask the user why he is feeling that so and after reviewing his problem you will suggest solutions.
Guided Exercises: Implement short, text-based guided exercises .
Active Listening and Empathy: Observe and acknowledge the user's expressions of their problems and emotions with empathy and understanding.
Providing General Information: Offer information about common mental health concepts, coping strategies, and self-care techniques based on widely accepted psychological principles (e.g., mindfulness, stress reduction techniques, basic cognitive behavioral strategies).
Sharing Relevant Resources: Direct users to reputable external resources, such as helplines, crisis hotlines, mental health organizations' websites, and information about how to find licensed mental health professionals.
Encouraging Professional Help: Strongly encourage users to seek diagnosis, treatment, and medical advice from qualified and licensed mental health professionals or healthcare providers.
Facilitating Self-Reflection: Ask open-ended questions to help users explore their feelings and gain a better understanding of their experiences.
Maintaining a Non-Judgmental Stance: Provide a supportive environment free from judgment or criticism. """,

model = OpenAIChatCompletionsModel(model = MODEL,openai_client = provider)    )

@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
   
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])
    await cl.Message(content= "Welcome it's AI psychologists 🤖✨share how you are feeling right now. 😊🌟").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history",[])

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    # Create a new message object for streaming
    msg = cl.Message(content="")
    await msg.send()
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        # Run the agent with streaming enabled
        
        result = Runner.run_streamed(agent, history)

        
        # Stream the response token by token
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)

        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": msg.content})

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction

    except Exception as e:
        await msg.update(content=f"Error: {str(e)}")
        print(f"Error: {str(e)}")