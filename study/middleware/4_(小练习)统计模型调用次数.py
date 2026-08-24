from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
'''
需求：利用中间件做一个统计模型调用次数的功能
'''


def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
                      )

r = agent.invoke({"messages": [HumanMessage(content="现在几点")]})

print(r['call_count'])


