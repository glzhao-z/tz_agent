from deepagents import create_deep_agent
from conn.llm import get_llm
from subA import get_agent as get_subA_agent
from subB import get_agent as get_subB_agent


agent = create_deep_agent(
    model=get_llm(), # 模型, 传一个llm实例
    tools=[], # 工具集
    system_prompt="你是一个助手", # 系统提示词
    subagents=[get_subA_agent(),get_subB_agent()]
)

res = agent.stream({"messages":[{"role":"user","content":"给我随机数"}]})
for chunk in res:
    print(chunk)

