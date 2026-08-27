from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import ToolMessage
from utils.doc_utils import os_utils as ou
from base import config as cfg
from uuid import uuid4
from utils.general_utils.loggers import logger
from os.path import normpath as np



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

    # wrap_tool_call的中间件
    # 如果包含root_dir，就消掉即可。
    async def awrap_tool_call(self,request,handler):
        response = await handler(request) # 调用工具
        # 边界情况1 判断工具的返回是否是ToolMessage：
        logger.info(type(response))
        if type(response)==ToolMessage:
            # 边界情况2 判断它是否有值且是字符串
            if response.content and type(response.content) is str:
                # 边界情况3 要规划化路径字符串中的 分隔符 /
                # 怎么工具返回中的内容
                response.content = np(response.content).replace(cfg.ROOT_PATH_AGENT,'')
            # 消掉root_dir
            return response


if __name__ == '__main__':
    pass