from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("api key error : fix your api key")

external_client = AsyncOpenAI(base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",api_key = GEMINI_API_KEY)
model = OpenAIChatCompletionsModel(openai_client = external_client,model = 'gemini-2.0-flash')
gemini_config = RunConfig(model_provider = external_client,model=model,tracing_disabled=True)
