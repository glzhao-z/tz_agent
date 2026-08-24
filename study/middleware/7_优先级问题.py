from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import wrap_model_call

@wrap_model_call
def wrap1(request, handle):
    print("wrap1_start")
    response = handle(request) # 调用模型
    print("wrap1_end")
    return response #必须返回response

@wrap_model_call
def wrap2(request, handle):
    print("wrap2_start")
    response = handle(request) # 调用模型
    print("wrap2_end")
    return response #必须返回response

'''
A:
wrap1_start
wrap1_end
wrap2_start
wrap2_end

B: 
wrap2_start
wrap2_end
wrap1_start
wrap1_end

C:
wrap1_start
wrap2_start
wrap2_end
wrap1_end

D:
wrap2_start
wrap1_start
wrap1_end
wrap2_end

E:
wrap1_start
wrap2_start
wrap1_end
wrap2_end
'''





def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
                 middleware=[wrap1,wrap2] # 传入中间件列表
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