from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled,AsyncOpenAI,function_tool
from agents.repl import run_demo_loop
from dotenv import load_dotenv
import requests
from dataclasses import dataclass
import os
import chainlit as cl

load_dotenv()

BASE_URL ="https://openrouter.ai/api/v1"
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"

router_api_key= os.getenv('ROUTER_API_KEY')
set_tracing_disabled(disabled = True)

provider = AsyncOpenAI(
    base_url = BASE_URL,
    api_key = router_api_key
)

MODEL = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client = provider
)

@dataclass
class LocationInfo:
    ip: str
    city: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    org:str

    def __str__(self):
        """Return a formatted string representation of the location info."""
        return f"""📡 **IP Geolocation Info**
- 🌐 IP: `{self.ip}`
- 🏙 City: **{self.city}**, {self.region}
- 🌍 Country: **{self.country}**
- 📍 Location: `{self.latitude}, {self.longitude}`
- 🕒 Timezone: `{self.timezone}`
- 🏢 Organization: {self.org}
"""

@function_tool
async def get_location_info(ip: str) -> LocationInfo:
    """
    Fetches geolocation information for a given IP address.
    
    Args:
        ip (str): The IP address to look up.
        
    Returns:
        LocationInfo: A dataclass containing the geolocation details.
    """

    url = f"https://ipapi.co/{ip or ''}/json/"
    response = requests.get(url)
    data = response.json()

    return LocationInfo(
        ip=data.get("ip", "N/A"),
        city=data.get("city", "N/A"),
        region=data.get("region", "N/A"),
        country=data.get("country", "N/A"),
        latitude=float(data.get("loc", "0,0").split(",")[0]),
        longitude=float(data.get("loc", "0,0").split(",")[1]),
        timezone=data.get("timezone", "N/A"),
        org=data.get("org", "N/A")
    )

agent = Agent(
    name="GeoLocationAgent",
    instructions="You are a helpful agent, if the user ask about gelocation of ip addresses use tool 'get_location_info' and return a formated beutiful output using LocationInfo dataclass.",
    model=MODEL,
    tools=[get_location_info],
    output_type=LocationInfo,
    tool_use_behavior="required",)





@cl.on_chat_start
async def on_chat_start():
    """Greet the user when the chat starts."""
    await cl.Message("Hello! I am your GeoLocation Agent. Ask me about the geolocation of any IP address 🌍").send()

    cl.user_session.set("history", [])
    cl.user_session.set("agent", agent)

@cl.on_message
async def handle_message(message: cl.Message):
    """Handle user messages and interact with the agent."""
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})
    cl.user_session.set("history", history)
    agent = cl.user_session.get("agent", None)

    # Run the agent with the user's message
    result = await Runner.run(agent, input=history)
    output = result.final_output
    if isinstance(output, LocationInfo):
        # Format the output using the LocationInfo dataclass
        await cl.Message(content=str(output)).send()
    else:
        await cl.Message("Sorry, I couldn't retrieve the geolocation information.").send()
    # Send the response back to the user
