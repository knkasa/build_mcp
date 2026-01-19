from mcp.server.fastmcp import FastMCP

# IMPORTANT: silence stdout logging
server = FastMCP(
    "example-mcp",
    log_level="ERROR",   # <- critical
)

@server.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@server.tool()
def hello(name: str) -> str:
    """Say hello to a user"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    server.run(transport="stdio")


'''
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="Example MCP Server")

class ToolSpec(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


def add_numbers(a: int, b: int) -> int:
    return a + b

def hello(name: str) -> str:
    return f"Hello, {name}!"

TOOLS = {
    "add_numbers": {
        "spec": ToolSpec(
            name="add_numbers",
            description="Add two numbers together",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
        ),
        "fn": add_numbers,
    },
    "hello": {
        "spec": ToolSpec(
            name="hello",
            description="Say hello to a user",
            parameters={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
            },
        ),
        "fn": hello,
    },
}

@app.get("/tools")
def list_tools():
    return {
        "tools": [tool["spec"].dict() for tool in TOOLS.values()]
    }

@app.post("/tools/invoke")
def invoke_tool(call: ToolCall):
    if call.name not in TOOLS:
        return {"error": f"Unknown tool: {call.name}"}

    result = TOOLS[call.name]["fn"](**call.arguments)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)
'''

