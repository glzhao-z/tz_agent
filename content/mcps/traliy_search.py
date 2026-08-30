from langchain_mcp_adapters.client import MultiServerMCPClient
from base import config as cfg
import asyncio

def get_tools():
    # 1. 定义mcp服务地址
    client = MultiServerMCPClient(
        {
            "search": {
                "transport": "streamable_http",
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={cfg.TAVILY_SEARCH_KEY}"
            }
        }
    )
    # 2. 得到mcp提供工具
    tools = asyncio.run(client.get_tools())
    return tools