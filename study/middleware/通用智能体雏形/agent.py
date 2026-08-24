
'''
planning and execute
计划与执行

'''
from langchain.agents import create_agent
import mytools as mt
from langchain_openai import ChatOpenAI
from todo_list_middle import TodoListMiddleware
def get_llm():
    llm = ChatOpenAI(
        #model="Qwen/Qwen3.5-27B",
        model ="Qwen/Qwen3.5-122B-A10B",
        base_url="https://api.siliconflow.cn/v1"
    )
    return llm


agent = create_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[mt.write_file,mt.read_file,mt.ls],
    middleware=[TodoListMiddleware()],
    system_prompt="你是一个助手", # 系统提示词

)

if __name__ == '__main__':
    res = agent.stream({"messages":[{"role":"user","content":"写个b.txt，随便写点什么"}]})
    for chunk in res:
        print(chunk)



