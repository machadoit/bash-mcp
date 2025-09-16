docker_image := "bash-mcp"

# Build the Docker image
build:
    docker build -t {{docker_image}} .

# Test with MCP Inspector
inspect *args: build
    npx @modelcontextprotocol/inspector docker run -i --rm \
        --network none \
        --user $(id -u):$(id -g) \
        --read-only \
        --tmpfs /tmp \
        --cap-drop ALL \
        --security-opt no-new-privileges \
        --name "{{docker_image}}-inspector" \
        -v "{{justfile_directory()}}/test-mcp-sandbox":/workdir/test-mcp-sandbox:ro \
        {{args}} \
        {{docker_image}}

# Interactive shell for development/debugging
dev *args: build
    docker run -it --rm \
        --network none \
        --user $(id -u):$(id -g) \
        --read-only \
        --tmpfs /tmp \
        --cap-drop ALL \
        --security-opt no-new-privileges \
        --entrypoint /bin/sh \
        -v "{{justfile_directory()}}/test-mcp-sandbox":/workdir/test-mcp-sandbox:ro \
        {{args}} \
        {{docker_image}}

# Run the actual MCP server (configration that you could use in the mcp settings of an agent)
serve: build
    docker run -i -d --rm \
        --network none \
        --user $(id -u):$(id -g) \
        --read-only \
        --tmpfs /tmp \
        --cap-drop ALL \
        --security-opt no-new-privileges \
        {{docker_image}}
