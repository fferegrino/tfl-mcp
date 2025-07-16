# MCP Client Demo

## Overview

This application demonstrates how a client interacts with an MCP (Model Control Protocol) server. The demo is built as a Streamlit application that communicates with an MCP server to manage interactions with the Anthropic API.

## Prerequisites

- An MCP server (located in the [_mcp-server_](../mcp-server) directory)
- Python and the UV package manager installed
- An Anthropic API key

## API Key Configuration

Before running the application, you need to set up your Anthropic API key:

1. Set the `ANTHROPIC_API_KEY` environment variable with your valid Anthropic API key
2. Alternatively, create a `.env` file in the project root with the following content:

   ```text
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running the Application

Execute the following command from the project root to start both the client and server:

```bash
uv run streamlit run app.py ../mcp-server/server.py
```

## Troubleshooting

If you encounter issues:

- Verify your Anthropic API key is valid and properly configured
- Ensure both the client and server components are running
- Check network connectivity between the client and server
