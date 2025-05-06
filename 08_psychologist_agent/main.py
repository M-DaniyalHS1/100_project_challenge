from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,AsyncOpenAI,RunConfig
import os
from dotenv import load_dotenv
import asyncio
import chainlit as cl

load_dotenv()

set_tracing_disabled(disabled = True)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')


provider = AsyncOpenAI(
    api_key = OPENROUTER_API_KEY,
    base_url = "https://openrouter.ai/api/v1"
)
MODEL = "deepseek/deepseek-chat:free"

psychologist = Agent(
    name = 'psychologist',
    instructions = """You are a personalized supportive AI assistant specializing in mental well-being.

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

    model = OpenAIChatCompletionsModel(model = MODEL,openai_client = provider)


)

@cl.on_chat_start
async def shru():
    """This functions starts the chat with a welcome message and creates a empty history list."""
    cl.user_session.set("history",[])
    await cl.Message(content = "Assalamo-a-Alaikum! My name is Dani, AI psychologists 🤖✨share how you are feeling right now. 😊🌟").send()

@cl.on_message
async def darmyan(message:cl.Message):
    """   
    Handle incoming user messages
    - Maintains conversation history
    - Processes message through the AI agent
    - Updates history with response
    - Sends response back to user
    """

    history = cl.user_session.get("history")
    history.append({"role":"user","content":message.content})

    result = await Runner.run(
        starting_agent = psychologist,
        input = history
    )

    history.append({"role":"system","content":result.final_output})

    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()