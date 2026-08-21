from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime


agent  = create_agent(model=get_llm() ,#模型
             tools=[datetime.datetime.now],#工具列表
             system_prompt='你是一个助理' )#系统提示词

r = agent.invoke({"messages": [HumanMessage(content="现在几点")]})
print(r['messages'][-1].content)

print(r)