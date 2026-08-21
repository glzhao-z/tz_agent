from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage



def add(a:int,b:int):
    """加法函数
    :param a: int 第一个加数
    :param b: int 第二个加数
    :return: int 两个数的和
    """
    return a+b


agent  = create_agent(model=get_llm() ,#模型
             tools=[add],#工具列表
             system_prompt='你是一个助理' )#系统提示词


r = agent.invoke({"messages": [HumanMessage(content="3+4等于多少")]})
print(r['messages'][-1].content)

print(r)