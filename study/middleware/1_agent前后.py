from langchain.agents import create_agent, middleware
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import before_agent,after_agent

# 中间件函数
@before_agent
def before_agent_function(state,runtime):
    print("Before agent state:", state)
    print("Before agent runtime:", runtime)

@after_agent
def after_agent_function(state,runtime):
    print("After agent state:", state)
    print("After agent runtime:", runtime)

def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             middleware=[before_agent_function,after_agent_function] # 传入中间件列表
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