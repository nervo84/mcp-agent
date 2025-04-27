import asyncio
import os
from dotenv import load_dotenv

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env
load_dotenv()

# Settings
MODEL_NAME = "gpt-4o"
PROMPT_MESSAGE = "Analyze how revenue of MSFT is changing over time."
SERVER_COMMAND = "python"
SERVER_ARGS = ["mcp_server.py"]

async def setup_agent(read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await load_mcp_tools(session)
        
        # Read OpenAI API Key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        model = ChatOpenAI(model=MODEL_NAME, openai_api_key=openai_api_key)
        agent = create_react_agent(model, tools)
        return agent

async def main():
    server_params = StdioServerParameters(command=SERVER_COMMAND, args=SERVER_ARGS)

    async with stdio_client(server_params) as (read, write):
        agent = await setup_agent(read, write)
        response = await agent.ainvoke({"messages": PROMPT_MESSAGE})
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
