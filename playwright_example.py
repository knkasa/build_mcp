# Make sure these are installed.
#node --version   # >= 18
#npm --version

# Install and run
#npx @modelcontextprotocol/server-playwright

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI  # or ChatBedrock

async def main():
    # 1. Connect to Playwright MCP server
    mcp_client = MultiServerMCPClient(
        servers={
            "playwright": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-playwright"],
                "transport": "stdio",
            }
        }
    )

    # 2. LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # 3. Create agent with MCP tools
    agent = create_agent(
        llm=llm,
        tools=mcp_client.get_tools()
    )

    # 4. Ask the agent to browse
    prompt = """
    Go to https://example.com
    Extract the page title and the main heading.
    """

    result = await agent.ainvoke(prompt)
    print(result)

asyncio.run(main())


