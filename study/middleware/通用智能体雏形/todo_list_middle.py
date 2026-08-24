from langchain.agents.middleware import AgentState, AgentMiddleware, ModelRequest, ModelResponse, ExtendedModelResponse
from pydantic import BaseModel,Field
from typing import Literal, Callable
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.tools import InjectedToolCallId
from typing import Annotated

'''
1. 产生一个todo list 任务列表。
列表中的每个任务，需要包含两个2东西。描述，状态(排队，正在处理，已完成)。
1.1 什么时候产生。 after_model
1.2 放哪里。done

2. 怎么去更新任务列表。 (写任务列表)
2.1 什么时候去调用工具更新todos,答llm自己定夺

3. 怎么让Agent做事时，根据任务列表。 (读任务列表) -> 把每次更新的任务列表放入上下文
'''

class Todo(BaseModel):
    description: str = Field(..., description="任务的描述")
    status: Literal["排队", "正在处理", "已完成"] = Field(..., description="任务的状态")

class Todos(AgentState):
    todos: list[Todo]


def write_todos(todos: list[Todo], tool_call_id:Annotated[str, InjectedToolCallId]):
    """
    创建或更新任务列表
    :param todos: 任务列表
    :return: command
    """
    return Command(update={"todos": todos,
                           "messages":[ToolMessage(content=f"任务列表已更新,当前列表:{todos}", tool_call_id=tool_call_id)]}
                   )


class TodoListMiddleware(AgentMiddleware):

    state_schema = Todos
    tools = [write_todos]
    def __init__(self):
        super().__init__()
        # 内置prompt让llm产生以及更新任务列表
        self.system_prompt = """
                先将用户的需求拆解为一个任务列表。
                每次工作时，查看任务列表。
                每做完1个任务，更新任务列表中当前任务的状态到 完成。
                """
    async def awrap_model_call(self,request,handler) :
        # 把任务中间里内置system_prompt加到request里面的state的messages里去
        request.system_prompt += '\n\n'+ self.system_prompt
        return await handler(request)