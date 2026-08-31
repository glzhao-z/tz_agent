from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

def get_tools():
    # 1. 定义mcp服务地址
    client = MultiServerMCPClient(
        {
            "excel": {
                "command": "uvx",
                "args": ["--index-url", "https://pypi.tuna.tsinghua.edu.cn/simple",
                         "excel-mcp-server", "stdio"],
                "transport": "stdio",
            }
        }
    )
    # 2. 得到mcp提供工具
    tools = asyncio.run(client.get_tools())
    return tools