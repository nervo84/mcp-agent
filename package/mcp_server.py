import logging
import yfinance as yf
from fastmcp import FastMCP
from pandas import DataFrame

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Instantiate the MCP server with the name "stocks"
mcp = FastMCP("stocks")

# Define a tool to fetch general company information
@mcp.tool()
def fetch_stock_info(symbol: str) -> dict:
    """Fetch general information about a company."""
    logger.info(f"Fetching info for symbol: {symbol}")
    # Add debugging to ensure the function is being called properly
    print(f"DEBUG: Fetching info for {symbol}") 
    stock = yf.Ticker(symbol)
    return stock.info

# Define a tool to fetch quarterly financial data
@mcp.tool()
def fetch_quarterly_financials(symbol: str) -> DataFrame:
    """Fetch quarterly financial statements of a company."""
    logger.info(f"Fetching quarterly financials for symbol: {symbol}")
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

# Define a tool to fetch annual financial data
@mcp.tool()
def fetch_annual_financials(symbol: str) -> DataFrame:
    """Fetch annual financial statements of a company."""
    logger.info(f"Fetching annual financials for symbol: {symbol}")
    stock = yf.Ticker(symbol)
    return stock.financials.T

# Main function to start the MCP server
def main():
    logger.info("Starting MCP server...")
    mcp.run(transport="stdio")

# Entry point of the program
if __name__ == "__main__":
    main()
# The MCP server will run and listen for requests on standard input/output.
# The tools can be called from a client using the MCP protocol.
# The server will log the requests and responses for debugging purposes.
# The server can be stopped by terminating the process (e.g., Ctrl+C in the terminal).
# The server is designed to be lightweight and efficient, making it suitable for real-time applications.
# The server can be extended with additional tools as needed.