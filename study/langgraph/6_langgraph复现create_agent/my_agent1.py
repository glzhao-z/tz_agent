from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict, Annotated # 导入类型定义工具
import operator # 导入操作符
from langchain.messages import AnyMessage, SystemMessage,ToolMessage
#from langgraph.prebuilt import ToolNode

class State(TypedDict):
    messages:Annotated[list[AnyMessage], operator.add] #消息列表，用于存储对话历史
    # Annotated[参数类型，参数的更新方式] 添加类型注解
    # list[AnyMessage] # 列表类型
    # operator.add 列表的更新方式，添加元素

def create_agent(system_prompt,tools,model):
    agent = StateGraph(State) # 先声明图，定义状态类型

    # ReAct的system_prompt
    default_system_prompt = """
    你是一个智能助手，使用ReAct（Reasoning and Acting）模式解决问题。请按照以下步骤思考：

    1. 思考(Thought)：分析问题，决定下一步行动
    2. 行动(Action)：调用工具或回答问题
    3. 观察(Observation)：获取工具执行结果

    以下是用户自定义的system_prompt:
    """
    system_prompt = default_system_prompt + system_prompt # 添加默认系统提示词
    model = model.bind_tools(tools) # 绑定工具

    tools_by_name = {tool.name: tool for tool in tools}  # 工具注册字典
    # 系统提示词如何作用
    def model_node(state:State): #模型节点，执行模型
        messages = [SystemMessage(content=system_prompt)] + state['messages'] # 添加系统提示词
        ai_reply = model.invoke(messages) # 调用模型
        return {"messages": [ai_reply]} # 把模型回复加进状态里的messages

    def tool_node(state:State):
        """执行工具调用"""
        result = []
        for tool_call in state["messages"][-1].tool_calls: # 遍历工具调用,有可能不止一个
            tool = tools_by_name[tool_call["name"]]  # 通过工具的名字获取工具
            observation = tool.invoke(tool_call["args"]) # 调用工具
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"])) # 添加工具执行结果到消息列表
            # 通过tool_call_id关联工具调用和工具执行结果
        return {"messages": result}

    # 怎么判断是否调用了工具
    def condinal_func(state:State):
        # 获取state中的messages中的最后一个消息
        last_message = state['messages'][-1]
        if last_message.tool_calls: # 判断是否调用了工具
            return "continue"
        else:
            return "break"

    agent.add_node("model", model_node) # 添加模型节点
    agent.add_node("tools", tool_node) # 添加工具节点

    agent.add_edge(START, "model")
    agent.add_conditional_edges("model", condinal_func, {"continue": "tools", "break": END})
    agent.add_edge("tools", "model") # 工具执行后，调用模型继续思考

    graph = agent.compile()
    return graph



