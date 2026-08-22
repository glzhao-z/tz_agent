from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime

def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' )#系统提示词

graph_image = agent.get_graph().draw_mermaid_png()
image_path = "agent.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

r = agent.invoke({"messages": [HumanMessage(content="现在几点")]})
print(r['messages'][-1].content)

print(r)