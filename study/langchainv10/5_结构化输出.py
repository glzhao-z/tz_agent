from langchain.agents import create_agent
from conn.llm import get_llm
from langchain.messages import HumanMessage
# 1. 定义结构化数据模板
from pydantic import BaseModel,Field

class ContactInfo(BaseModel):
    name: str = Field(..., description="联系人姓名")
    phone: str = Field(..., description="联系人电话")
    email: str = Field(..., description="联系人邮箱")

# 2. 把结构化模板通过response_format的参数交给creat_agent

agent  = create_agent(model=get_llm() ,#模型
             tools=[],#工具列表
             response_format=ContactInfo,
             system_prompt='你是一个助理' )#系统提示词


r = agent.invoke({"messages": [HumanMessage(content="从如下文本中提取信息: John Doe, john@example.com, (555) 123-4567")]})
print(r)

# 3. 通过structured_response的key获取结构化的值

print(r['structured_response'])
print(type(r['structured_response']))
print(r['structured_response'].name)