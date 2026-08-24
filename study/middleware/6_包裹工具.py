from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import wrap_tool_call,ToolCallRequest
from typing import Callable
from langchain.messages import ToolMessage
from langgraph.types import Command

@wrap_tool_call
def wrap_tool_call_function(request,
                            handle):
    print("Tool request:", request)
    toolMessage = handle(request) # 调用工具
    print("Tool Message:", toolMessage)
    return toolMessage #必须返回ToolMessage,也就是调用工具的响应结果


def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             middleware=[wrap_tool_call_function] # 传入中间件列表
                      )

graph_image = agent.get_graph().draw_mermaid_png()
image_path = "agent.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

r = agent.stream({"messages": [HumanMessage(content="现在几点")]})

for rr in r:
    print(rr)

# print(r['messages'][-1].content)
# print(r)