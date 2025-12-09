# import MCP library
from mcp import types as mcp_types
from mcp.server.lowlevel import Server , NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio as stdio_server

import asyncio

#ADK tool import
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.load_web_page import load_web_page

# ADK tool <-> MCP server uttlityl
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type


async def echo_tool(args: dict) -> dict:
    # just return same message
    msg = args.get("message", "")
    return {"echo": msg}

def create_mcp_server():
    app = Server("simple-adk-mcp-server")

    @app.list_tools()
    async def list_tools() -> list[mcp_types.Tool]:
        return [
            mcp_types.Tool(
                id = "echo",
                name = "echo",
                description = "Echo back a message",
                arguments_schema = mcp_types.JSONSchema(
                    type="object",
                    properties={
                        "message": {"type": "string", "description": "Message to echo"}
                    },
                    required=["message"]
                ),
                return_schema = mcp_types.JSONSchema(
                    type="object",
                    properties={
                        "echo": {"type": "string", "description": "Echoed message"}
                    },
                    required=["echo"]
                ),
            )
        ]
    @app.call_tool()
    async def call_tool(id: str, arguments: dict) -> list[mcp_types.Content]:
        if id == "echo":
            result = await echo_tool(arguments)
            # Return as JSON content
            return [mcp_types.JSONContent(value=result)]
        else:
            raise Exception(f"Unknown tool: {id}")

    return app

if __name__ == "__main__":
    server = create_mcp_server()
    stdio_server.serve(server)