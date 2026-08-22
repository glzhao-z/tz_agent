from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class State(TypedDict):
    messages:list #消息列表，用于存储对话历史


def create_agent(system_prompt,tools,model):
    agent = StateGraph(State)

    def model_node(state): #模型节点，执行模型
        return model.invoke(state['messages'])
        
    def tool_node(state): #工具节点
        # 根据state中的信息选择工具
        return 工具的执行结果

    def condinal_func(state):
        return "continue" if state['记录是否调用工具']  else "break"


    agent.add_node("model", model_node)
    agent.add_node("tools", tool_node)
    agent.add_edge(START, "model")
    agent.add_conditional_edges("model", condinal_func, {"continue": "tools", "break": END})


    return agent.compile()