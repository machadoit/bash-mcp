#Example file from https://github.com/jlowin/fastmcp
from fastmcp import FastMCP, Context
import sys
import subprocess

mcp = FastMCP("Demo 🚀")

@mcp.tool
async def add(a: int, b: int, ctx: Context) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
async def bash(command: str, ctx: Context) -> str:
    """Execute a bash command and return its output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    mcp.run()
