from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import wrap_tool_call,ToolCallRequest,AgentState
from typing import Callable
from langchain.messages import ToolMessage
from langgraph.types import Command

class MyState(AgentState):
    stop_reason: str

def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

def stop_command():
    """停止命令"""
    print('1111')
    return "已停止"

@wrap_tool_call
def auto_stop(request,handler) -> ToolMessage | Command:
    tool_name = request.tool_call['name']

    # 如果是 stop_command，结束并更新自定义字段
    if tool_name == "stop_command":
        print("🛑 检测到停止命令，直接结束")
        return Command(
            goto="__end__",
            update={"stop_reason": "用户叫停止的"}  # 更新自定义字段
        )

    # 其他工具正常执行
    return handler(request)



agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time,stop_command],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             middleware=[auto_stop], # 传入中间件列表
             state_schema=MyState
                      )

graph_image = agent.get_graph().draw_mermaid_png()
image_path = "agent.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

r = agent.stream({"messages": [HumanMessage(content="去触发一下停止命令")]})

for rr in r:
    print(rr)

# print(r['messages'][-1].content)
# print(r)