
'''
planning and execute
计划与执行

'''
from langchain.agents import create_agent
import mytools as mt
from langchain_openai import ChatOpenAI
from conn.llm import get_llm

# def get_llm():
#     llm = ChatOpenAI(
#         model="Qwen/Qwen3-Next-80B-A3B-Instruct",
#         base_url="https://api.siliconflow.cn/v1"
#     )
#     return llm


agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[mt.write_file,mt.read_file,mt.ls],
    system_prompt="你是一个助手", # 系统提示词

)

res = agent.stream({"messages":[{"role":"user","content":"写个b.txt，随便写点什么"}]})
for chunk in res:
    print(chunk)



