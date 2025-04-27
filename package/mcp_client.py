import asyncio
import os
import logging
from dotenv import load_dotenv

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Settings
MODEL_NAME = "gpt-4.1"
PROMPT_MESSAGE = "Analyze how revenue of MSFT is changing over time."
SERVER_COMMAND = "python"
SERVER_ARGS = ["mcp_server.py"]

async def setup_agent(read, write):
    try:
        logger.debug("Setting up agent...")
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            
            # Read OpenAI API Key from environment
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            
            logger.debug(f"Loaded OpenAI API key: {openai_api_key}")
            model = ChatOpenAI(model=MODEL_NAME, openai_api_key=openai_api_key)
            agent = create_react_agent(model, tools)
            logger.debug("Agent setup complete.")
            return agent
    except Exception as e:
        logger.error(f"Error setting up agent: {e}")
        raise

async def main():
    logger.debug("Starting the main function...")
    server_params = StdioServerParameters(command=SERVER_COMMAND, args=SERVER_ARGS)
    
    try:
        async with stdio_client(server_params) as client:
            read, write = client  # Unpack della tupla qui
            logger.debug("Connected to server, setting up agent...")
            agent = await setup_agent(read, write)
            logger.debug("Agent setup successful. Invoking agent...")
            response = await agent.ainvoke({"messages": PROMPT_MESSAGE})
            logger.debug(f"Agent response: {response}")
            print(response)
    except Exception as e:
        logger.error(f"Error in main: {e}")

def run_main():
    """Wrapper per eseguire il codice asincrono quando chiamato da Poetry."""
    try:
        logger.debug("Running main through Poetry...")
        return asyncio.run(main())
    except Exception as e:
        logger.error(f"Error in run_main: {e}", exc_info=True)
        return 1  # Ritorna un codice di errore

if __name__ == "__main__":
    logger.debug("Running main...")
    asyncio.run(main())
