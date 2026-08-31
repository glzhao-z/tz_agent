from deepagents import create_deep_agent
from conn.llm import get_llm
from subA import get_agent


agent = create_deep_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    subagents=[get_agent()]
)

res = agent.stream({"messages":[{"role":"user","content":"现在几点"}]})
for chunk in res:
    print(chunk)

