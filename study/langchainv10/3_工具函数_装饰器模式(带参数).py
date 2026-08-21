from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
from langchain.tools import tool

# 方法一：使用 Pydantic 模型定义参数
# from pydantic import BaseModel, Field
#
# class Args(BaseModel):
#     a: int = Field(description="第一个加数")
#     b: int = Field(description="第二个加数")
# @tool(description="用以加法的函数",args_schema=Args)

# 方法二：使用字典定义参数
@tool(description="用以加法的函数",args_schema={"a":{"description":"第一个加数","type":"integer"},
                                                "b":{"description":"第二个加数","type":"integer"}})
def add(a:int,b:int):
    print("add函数被调用")
    return a+b


agent  = create_agent(model=get_llm() ,#模型
             tools=[add],#工具列表
             system_prompt='你是一个助理' )#系统提示词

# r = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})


r = agent.invoke({"messages": [HumanMessage(content="3+4等于多少")]})
print(r['messages'][-1].content)

print(r)