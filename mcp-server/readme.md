# MCP Server demo

## Overview

This application demonstrates how to setup an MCP Server using the [mcp-server](https://github.com/modelcontextprotocol/mcp-server) library.

MCP allows AI models to access external tools and data sources through a standardized protocol, enhancing their capabilities beyond their training data.

The MCP Server in this demo provides a bridge to the Transport for London (TfL) API, allowing AI models to access real-time transportation data and services across London's public transport network.

## Prerequisites

- Python and the UV package manager installed
- In theory you would need a TfL API key, but for basic functionality as this demo uses publicly accessible endpoints, you should be able to run the server without one

## Running the server

Under the current setup (the server uses the `stdio` transport), the server does not need to be run manually, instead it is run by the client application.

However, I found it useful to run the server locally to debug the server, to run the server locally, you can use the following command:

```bash
uv run python server.py local
```

This will run the server in the current terminal, and you can modify the server code at `server.py` and see the changes in the terminal.
