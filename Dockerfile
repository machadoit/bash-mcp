FROM python:3.12-slim

# Install dependencies and clean up in single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends ripgrep && \
    pip install --no-cache-dir fastmcp markitdown[pdf] && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create app directory for MCP server code
WORKDIR /app
COPY server.py .
COPY ai-guides/ /ai-guides/

# Create workdir for mounted folders
WORKDIR /workdir

ENTRYPOINT ["python", "/app/server.py"]
