import yfinance as yf
from fastmcp import FastMCP
from pandas import DataFrame

mcp = FastMCP("stocks")

@mcp.tool()
def fetch_stock_info(symbol: str) -> dict:
    """Get Company's general information."""
    print(f"Fetching info for symbol: {symbol}")  # Log per debug
    stock = yf.Ticker(symbol)
    return stock.info

@mcp.tool()
def fetch_quarterly_financials(symbol: str) -> DataFrame:
    """Get stock quarterly financials."""
    print(f"Fetching quarterly financials for symbol: {symbol}")  # Log per debug
    stock = yf.Ticker(symbol)
    return stock.quarterly_financials.T

@mcp.tool()
def fetch_annual_financials(symbol: str) -> DataFrame:
    """Get stock annual financials."""
    print(f"Fetching annual financials for symbol: {symbol}")  # Log per debug
    stock = yf.Ticker(symbol)
    return stock.financials.T

def main():
    print("Starting MCP server...")
    mcp.run(transport="stdio")
    print("MCP server is running.")

if __name__ == "__main__":
    main()
