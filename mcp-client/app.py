import streamlit as st
import sys
from contextlib import AsyncExitStack
from mcp.client.stdio import stdio_client
import asyncio
import nest_asyncio
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
import json
import os

from dotenv import load_dotenv

st.set_page_config(layout="wide")

load_dotenv()

server = sys.argv[1]

if not "ANTHROPIC_API_KEY" in os.environ:
    st.error("ANTHROPIC_API_KEY is not set")
    st.stop()

anthropic = Anthropic()

# Monkey patch Streamlit's internal event loop
nest_asyncio.apply()

loop = asyncio.get_event_loop()


exit_stack = AsyncExitStack()


def get_mcp_session():
    server_params = StdioServerParameters(command="python", args=[server], env=None)
    stdio, write = loop.run_until_complete(exit_stack.enter_async_context(stdio_client(server_params)))
    session = loop.run_until_complete(exit_stack.enter_async_context(ClientSession(stdio, write)))
    loop.run_until_complete(session.initialize())
    return session


session = get_mcp_session()


server_response = loop.run_until_complete(session.list_tools())

st.title("MCP Client")
left_col, right_col = st.columns([2, 3], gap="large")

with left_col:
    st.write(f"Connected to _{server}_")
    query = st.text_input("Query")

with right_col:
    st.markdown(f"#### Available tools in _{server}_")
    for tool in server_response.tools:
        with st.expander(tool.name):
            st.write(tool)

    if query:
        messages = [{"role": "user", "content": query}]
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in server_response.tools
        ]

        st.markdown("#### First interaction with the LLM")
        st.write(messages[0])
        # st.write(available_tools)

        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
        )

        st.markdown("#### Initial response from the LLM")
        st.write(response.content)

        final_text = []
        assistant_message_content = []
        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                result = loop.run_until_complete(session.call_tool(tool_name, tool_args))
                assistant_message_content.append(content)

                messages.append({"role": "assistant", "content": assistant_message_content})
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result.content,
                            }
                        ],
                    }
                )

                st.markdown(f"#### Result of calling `{tool_name}`")
                st.code(json.dumps(tool_args))

                st.write(result.content)

                response = anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools,
                )

                final_text.append(response.content[0].text)

        st.markdown("#### Messages sent to the LLM")
        st.write(messages)

        st.subheader("Final response")
        st.text("\n".join(final_text))
