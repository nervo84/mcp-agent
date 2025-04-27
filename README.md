# MCP Agent
An MCP (Model Context Protocol) server and client using FastMCP and LangChain. 

You can watch the video on how it was built on my [YouTube](https://youtu.be/3K39NJbp2IA).


Follow me for updates and future projects:
👉 [LinkedIn](https://www.linkedin.com/in/salvatore-postiglione-927179aa/)
👉 [X (Twitter)](https://x.com/postiglionesax)

# Pre-requisites

Install the dependencies with poetry:

```bash
poetry install
```

Generate an OpenAI API key and set the OPENAI_API_KEY environment variable:

```bash
export OPENAI_API_KEY=...
```
(On Windows, use set instead of export)

# Run
Run the application:

```bash
poetry run mcp_client.py
```