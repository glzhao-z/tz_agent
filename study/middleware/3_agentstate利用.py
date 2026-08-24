from langchain.agents import create_agent, middleware
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import before_agent,after_agent,before_model,after_model

# 自定义的state继承AgentState
from langchain.agents import AgentState
class MyState(AgentState):
    start_time: datetime.datetime
    end_time: datetime.datetime
    duration: datetime.timedelta


# 中间件函数
@before_agent
def before_agent_function(state,runtime):
    state['start_time'] = datetime.datetime.now()
    print("Before agent state:", state)
    print("Before agent runtime:", runtime)
    return state

@after_agent
def after_agent_function(state,runtime):
    print("After agent state:", state)
    print("After agent runtime:", runtime)
    state['end_time'] = datetime.datetime.now()
    state['duration'] = state['end_time'] - state['start_time']
    return state

@before_model
def before_model_function(state:MyState,runtime):
    print("Before model")
    return state

@after_model
def after_model_function(state,runtime):
    print("After model")
    return state

def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             middleware=[before_agent_function,after_agent_function,before_model_function,after_model_function], # 传入中间件列表
             state_schema=MyState # 传入自定义状态
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