from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage,AIMessageChunk
import datetime

def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' )#系统提示词

r = agent.stream({"messages": [HumanMessage(content="现在几点")]},stream_mode=["messages","updates"])
for a in r:
    # 1.保留updates信息
    # 2.提炼messages信息 -> AIMessageChunk -> content
    # 如何分开处理updates与messages，答：用一个if判断它是updates还是messages
    if a[0]=='updates':
        print(a)
    else:
        #如果不是updates则代表它是messages，则需要走messages的处理逻辑
        # 首先拿AIMessageChunk
        chunk = a[1][0]
        # 小需求1：屏蔽toolmessage
        # 判断这个chunk是AimessageChunk还是ToolMessage
        if type(chunk)==AIMessageChunk:
            token = chunk.content
            # 小需求2：处理空格换行符.
            #  利用字符串的.strip()去除字符串两端的空格与换行符
            #  print()默认会打印出一个换行符,相当于end=\n，如果不想换行，仅需end=''
            print(token.strip(),end='')

# for a in r:
#     if a[0]=='messages':
#         if type(a[1][0])==AIMessageChunk:
#             token = a[1][0].content
#             if token.strip()!='':
#                 print(token,end='|')
#     else:
#         print(a)