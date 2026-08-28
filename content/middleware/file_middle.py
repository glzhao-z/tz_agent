import os.path,asyncio

from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import ToolMessage
from utils.doc_utils import os_utils as ou, base64_utils
from base import config as cfg
from uuid import uuid4
from utils.general_utils.loggers import logger
from os.path import normpath as np



class FileState(AgentState):
    before_paths:set
    upload_files:list

# 1. 初始化
# 2. 更新

class FileMiddle(AgentMiddleware):

    state_schema = FileState
    async def abefore_agent(self,state,runtime):
        dir = os.path.join(cfg.ROOT_PATH_AGENT, cfg.USER_UPLOAD_PATH)
        await asyncio.to_thread(os.makedirs,dir, exist_ok=True) # 创建目录
        # 判断是否有上传的文件
        if state.get('upload_files'):
            # 获取代表文件的数据
            for file in state['upload_files']:
                # 获取每个文件的base64字符串及文件名
                file_base64 = file['data']
                file_name = file['metadata']['filename']
                file_path = os.path.join(dir, file_name)
                # 解码并保存
                await asyncio.to_thread(base64_utils.decode_file,file_base64, file_path)


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

    def change_file_path(self,filepath):
        filepath = os.path.normpath(filepath)  # 规范化路径,把'\'给规范化成os.sep
        if cfg.ROOT_PATH_AGENT in filepath: # 如果路径本身就包含了根目录，则直接返回
            return filepath

        if os.path.isabs(filepath):  # isabs是判断这个路径是否是绝对路径，绝对路径的特征就是前面会有个/
            # relpath就是路径相对化，把绝对路径变成相对路径，其实也就是 去掉 start 的字符串
            filepath = os.path.relpath(filepath, start=os.sep)  # os.sep是一个规划话的分隔符 \
        p = os.path.join(cfg.ROOT_PATH_AGENT, filepath)
        return p


    # wrap_tool_call的中间件
    # 如果包含root_dir，就消掉即可。
    async def awrap_tool_call(self,request,handler):

        # # 在request里找到路径相关的参数
        for arg_key in request.tool_call['args']:
            if arg_key in ['filepath']:
                # 把root_dir添加上
                # /a.txt ->  /agent_files/a.txt
                request.tool_call['args'][arg_key] = self.change_file_path(request.tool_call['args'][arg_key])

        response = await handler(request) # 调用工具
        # 边界情况1 判断工具的返回是否是ToolMessage：
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