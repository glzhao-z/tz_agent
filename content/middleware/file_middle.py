
from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import ToolMessage


from utils.doc_utils import os_utils as ou
from base import config as cfg

class FileMiddle(AgentMiddleware):

    def before_model(self, state,runtime):
        # 把目录结构添加到上下文
        # 1. 得到目录结构字符串
        dir_str = ou.list_directory(path=cfg.ROOT_PATH_AGENT)
        # 2. 添加到上下文
        return {'messages':[ToolMessage(content=f'当前目录结构如下:\n{dir_str}',tool_call_id='directory_tool')]}