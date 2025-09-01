import asyncio
from agents import RunResult
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
import chainlit as cl
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
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

# Create MCP server params
mcp_params: MCPServerStreamableHttpParams = {
    "url": "http://127.0.0.1:8000/mcp",
    "headers": {"Authorization": "Bearer YOUR_TOKEN"},
    "timeout": timedelta(seconds=10),
    "sse_read_timeout": timedelta(minutes=3),
    "terminate_on_close": True
}

# Create MCP server instance
mcp_server1 = MCPServerStreamableHttp(params=mcp_params)

# Create an AI agent instance with a name and instructions
github_agent = Agent(
    name="github_agent",
    instructions="You are a GitHub-specialized agent that performs user GitHub tasks using MCP-provided tools.",
    model=model,
    mcp_servers=[mcp_server1]
)

# Test run with a sample question (synchronous)



async def main():
    # Your MCP server HTTP endpoint
    server_url = "http://localhost:8000"  # Change if needed

    print("🚀 Starting MCP Server Connection")
    print("=" * 50)

    # Connect to the MCP server over HTTP
    # Connect using streamable HTTP client
    async with streamablehttp_client("http://localhost:8000/mcp") as (read_stream, write_stream, get_session_id):
        async with ClientSession(read_stream, write_stream) as session:
            print("✅ Connected to MCP server!")

            init_result = await session.initialize()
            print(f"🔧 Server capabilities: {init_result.capabilities}")

            result =await Runner.run(
                input="what is the latest commit i have made on my repo call mcp tools to check",
                starting_agent=github_agent
                    )
            print(result.final_output)
           
#     print("Test Run Output:", result.final_output)
            # Optional: list available tools
            # tools_result = await session.list_tools()
            # for tool in tools_result.tools:
            #     print("Available tool: ",tool.name)


            # #calling git_commit tool
            # result = await session.call_tool(name = "git_diff_stagged",arguments ={ "repo_path":"D:/class11/100_project_challenge"})


            # Call the git_status tool
            # result = await session.call_tool(
            #     name="git_status",
            #     arguments={
            #         "repo_path": "D:/class11/100_project_challenge"  # Use forward slashes
            #     }
            # )
            # print("Result : ",result)
            # # Print the response
            # for item in result.content:
            #     if item.type == "text":
            #         print(item.text)
            #     else:
            #         print(item)
if __name__ == "__main__":
    asyncio.run(main())
