from langchain.agents import create_agent
from conn.llm import get_llm

agent  = create_agent(model=get_llm() ,#模型
             tools=[],#工具列表
             system_prompt='你是一个助理' )#系统提示词

r = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})

print(r)