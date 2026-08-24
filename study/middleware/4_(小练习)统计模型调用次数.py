from langchain.agents import create_agent,AgentState
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
from langchain.agents.middleware import before_model,before_agent

'''
需求：利用中间件做一个统计模型调用次数的功能
1. 有一个载体就记录这个调用次数 State -> AgentState
2. 在某一个中间件内去增加这个计数。before_model
3. 在哪里初始一下计数。before_agent
'''
class CallCountState(AgentState):
    call_count: int # 调用次数

@before_agent
def init_call_count(agent_state: CallCountState,runtime):
    return {"call_count":0}

@before_model
def call_count_middleware(agent_state: CallCountState,runtime):
   agent_state["call_count"]+=1
   return agent_state


def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             state_schema=CallCountState,
             middleware=[init_call_count,call_count_middleware]
                      )

r = agent.invoke({"messages": [HumanMessage(content="现在几点")]})

print(r['call_count'])


