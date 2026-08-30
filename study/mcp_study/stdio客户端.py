from conn.llm import get_llm
from langchain.agents import create_agent

from langchain_mcp_adapters.client import MultiServerMCPClient


# 1. 定义mcp服务地址
client = MultiServerMCPClient(
    {
        "demo1": {
            "transport": "stdio",
            "command": "python",
            "args": ["stdio_demo.py"]
        }
    },
)



import asyncio

# 2. 得到mcp提供工具
tools = asyncio.run(client.get_tools())
agent = create_agent(
        get_llm(),
        tools=tools
    )
a = asyncio.run(agent.ainvoke({"messages": [{"role": "user", "content": "2*3等于几"}]}))
print(a)


# async def do():
#
#     # 2. 得到mcp提供工具
#     tools = await client.get_tools()# 获取MCP工具
#
#
#     # 3. 工具传入agent
#     agent = create_agent(
#         get_llm(),
#         tools=tools
#     )
#     response = await agent.ainvoke(
#         {"messages": [{"role": "user", "content": "2*3等于几"}]}
#     )
#     print(response["messages"][-1].content)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(do())