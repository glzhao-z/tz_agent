from langchain.agents import create_agent
from langchain.tools import tool
import datetime
from conn.llm import get_llm
from langchain.agents.middleware import ModelCallLimitMiddleware

model_call_limit_middleware = ModelCallLimitMiddleware(
    run_limit=2,
    exit_behavior="end"
)


# ============ 定义工具 ============
@tool
def get_current_time():
    """获取当前时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ 创建 Agent（使用预设的 ModelCallLimitMiddleware） ============
agent = create_agent(
    model=get_llm(),
    tools=[get_current_time],
    middleware=[model_call_limit_middleware]
)

graph_image = agent.get_graph().draw_mermaid_png()
image_path = "agent.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)


# ============ 执行测试 ============
result = agent.stream(
    {"messages": [{"role": "user", "content": "现在几点？"}]},
)
for r in result:
    print(r)

