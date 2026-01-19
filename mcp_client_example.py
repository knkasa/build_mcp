import asyncio
import boto3
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_aws import ChatBedrock
from langchain_core.tools import StructuredTool

'''
langchain                 1.2.6
langchain-aws             1.2.1
langchain-core            1.2.7
langchain-mcp-adapters    0.2.1  ****better to use <0.2.0 (otherwise you'll need clean_mcp_tool() function.)  Fix may be coming later(2026/1/19)
langgraph                 1.0.6
langgraph-checkpoint      4.0.0
langgraph-prebuilt        1.0.6
langgraph-sdk             0.3.3
langsmith                 0.6.4
mcp                       1.25.0
modular-mcp               0.3.0
'''


def clean_mcp_tool(mcp_tool):
    """Use only if langchain-mcp-adapters>=0.2.0"""
    return StructuredTool(
        name=mcp_tool.name,
        description=mcp_tool.description,
        func=mcp_tool._run,
        coroutine=mcp_tool._arun,
        args_schema=mcp_tool.args_schema
    )

async def main():
    client = MultiServerMCPClient(
        {
            "local-mcp": {
                "transport": "stdio",
                "command": "python",
                "args":["mcp_server.py"]
            }
        }
    )

    tools = await client.get_tools()
    print("Loaded MCP tools:", [t.name for t in tools])
    fixed_tools = [clean_mcp_tool(t) for t in tools] # Only requires if using AWS Bedrock and langchain-mcp-adapters>=0.2.0

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id="",
        aws_secret_access_key="",
    )

    llm = ChatBedrock(
        client=bedrock_runtime,
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        model_kwargs={
            "temperature": 0.5,
            "max_tokens": 5000,
        },
    )

    agent = create_agent(
        model=llm,
        tools=tools,  #Use "tools" or "fixed_tools"
    )

    prompt = "Add 3 and 5 using the available tools."
    result = await agent.ainvoke({"messages": [("user", prompt)]})

    final_message = result["messages"][-1]
    print(final_message.content)


if __name__ == "__main__":
    asyncio.run(main())