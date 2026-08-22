from langchain.agents import create_agent
from langchain.messages import HumanMessage
import datetime
from langchain_openai import ChatOpenAI

def get_llm():
    llm = ChatOpenAI(base_url='https://api.siliconflow.cn/v1',
                     model='Qwen/Qwen3.5-27B')
    return llm


def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent1  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' )#系统提示词

if __name__ == '__main__':

    r = agent1.invoke({"messages": [HumanMessage(content="现在几点")]})
    print(r['messages'][-1].content)

    print(r)