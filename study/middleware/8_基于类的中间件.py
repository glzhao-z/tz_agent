from typing import Callable, Any

from langchain.agents import create_agent, middleware
from langchain.agents.middleware.types import ResponseT
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command
from langgraph.typing import ContextT

from conn.llm import get_llm
from langchain.messages import HumanMessage
import datetime
# 中间件导包
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse, ExtendedModelResponse


class MyMiddleware(AgentMiddleware):

    def before_agent(self,state,runtime):
        print("Before agent state:", state)
        print("Before agent runtime:", runtime)

    def after_agent(self,state,runtime):
        print("After agent state:", state)
        print("After agent runtime:", runtime)

    def before_model(self,state,runtime):
        print("Before model")
        return state

    def after_model(self,state,runtime):
        print("After model")
        return state

    def wrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]],
    ) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:
        print("Wrap model call")
        return handler(request)

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
    ) -> ToolMessage | Command[Any]:
        print("Wrap tool call")
        return handler(request)


def get_current_time():
    """获取当前时间"""
    return str(datetime.datetime.now())

agent  = create_agent(model=get_llm() ,#模型
             tools=[get_current_time],#工具列表
             system_prompt='你是一个助理' ,#系统提示词
             middleware=[MyMiddleware()] # 传入中间件列表
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