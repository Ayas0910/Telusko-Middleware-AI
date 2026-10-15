from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp_server = FastMCP("1st_MCP_Server")

mcp_server.run(transport = "stdio")


@mcp_server.tool
def greet()->str:
    """This is the tool to greet"""
    return "Hello from telusko.we hope you are fine?"
