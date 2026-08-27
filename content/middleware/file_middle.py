from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import ToolMessage
from utils.doc_utils import os_utils as ou
from base import config as cfg
from uuid import uuid4
from utils.general_utils.loggers import logger

class FileState(AgentState):
    before_paths:set

# 1. 初始化
# 2. 更新

class FileMiddle(AgentMiddleware):

    state_schema = FileState

    def before_model(self, state,runtime):
        # 把目录结构添加到上下文
        # 1. 得到目录结构字符串
        dir_str = ou.list_directory(path=cfg.ROOT_PATH_AGENT)
        current_paths = ou.get_all_files(directory=cfg.ROOT_PATH_AGENT)
        # before_paths的初始化
        # 两个判断满足其一就可做后面的动作(目录结构添加进上下文，以及更新状态中目录结构记录)
        # 1. 判断是否是第一次进来
        # 2. 判断是否目录结构有更新
        if (not state.get('before_paths')) or current_paths!=state['before_paths']:
            # 2. 添加到上下文
            return {'messages':[ToolMessage(content=f'当前目录结构如下:\n{dir_str}',tool_call_id=uuid4().hex)],
                    'before_paths':current_paths} # 更新目录结构记录


    # 每次得到目录结构后，记录于某一个日志系统中，想要区分每次打印结构的追踪标识