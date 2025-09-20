#Example file from https://github.com/jlowin/fastmcp
import os
import subprocess
from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP, Context

mcp = FastMCP("Tools to help you search and take notes! Includes PDF to Markdown Converter for better searches.")

@mcp.tool
async def bash(command: str, ctx: Context) -> str:
    """Execute a bash command and return its output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

@mcp.tool()
async def convert_pdf_to_markdown(
    pdf_filename: Annotated[str, Field(description="Name of the PDF file to convert relative to the PDF root directory")],
    ctx: Context,
    pdf_root: Annotated[str, Field(description="Root directory for PDF files")] = "docs-pdf",
    md_root: Annotated[str, Field(description="Root directory for markdown output")] = "docs-markdown"
) -> str:
    """Convert PDF to markdown.

    Converts a PDF file to markdown format and saves it to the specified output directory.
    The function handles path resolution and creates necessary directories automatically.

    Assumes relative paths for pdf_root and md_root from the working directory.
    """
    md_filename = pdf_filename.replace('.pdf', '.md')

    pdf_path = os.path.join(pdf_root, pdf_filename)
    md_path = os.path.join(md_root, md_filename)

    # Create output directory if needed
    md_dir = os.path.dirname(md_path)
    await ctx.debug(f"Ensuring directory {md_dir} exists")
    subprocess.run(['mkdir', '-p', md_dir])

    # Run markitdown command
    await ctx.info(f"Converting {pdf_path} to {md_path}")
    subprocess.run(['markitdown', pdf_path, '-o', md_path])

    return f"Converted {pdf_path} to {md_path}"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
