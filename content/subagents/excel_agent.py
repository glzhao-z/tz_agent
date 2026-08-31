from conn.llm import get_llm
from content.mcps import excel_mcp
from content.middleware import file_middle,rate_limit_middle
def get_agent():
    return {
        "name": "excel-agent",
        "description": "做Excel的助手",
        "system_prompt": f"你是一个做Excel的助手",
        "tools": excel_mcp.get_tools(),
        "model": get_llm(),
        "middleware":[file_middle.FileMiddle(),rate_limit_middle.anti_rate_limit]
    }