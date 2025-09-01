import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
import os

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure model
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# MCP server params
mcp_params: MCPServerStreamableHttpParams = {
    "url": "http://127.0.0.1:8000/mcp/",
    "timeout": timedelta(seconds=10),
    "sse_read_timeout": timedelta(minutes=3),
    "terminate_on_close": False
}

# Create MCP server instance
mcp_server_hello = MCPServerStreamableHttp(params=mcp_params)

async def main():

    while True:
        user_input = input("\n💬 how can i help u: ")

        if user_input.lower().strip() in {"exit", "quit"}:
            break
        else:
            try:
                # Connect the MCP server
                await mcp_server_hello.connect()

                # Create agent
                github_agent = Agent(
                    name="github_agent",
                    instructions="You are a GitHub-specialized agent that performs user GitHub tasks using MCP-provided tools.",
                    model=model,
                    mcp_servers=[mcp_server_hello]
                )
                # Run agent
                result = await Runner.run(
                    input=user_input,
                    starting_agent=github_agent
                )
                result = await Runner.run(
                    input=user_input,
                    starting_agent=github_agent
                )
                print("Agent Output:", result.final_output)


            finally:
                # Ensure MCP server is closed cleanly
                await mcp_server_hello.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
