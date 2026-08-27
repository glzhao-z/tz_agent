from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import AIMessage
from utils.doc_utils import zip_files as zf, os_utils as ou
from base import config as cfg
from conn import minio_conn as mc
import asyncio
import os
import time

class state(AgentState):
    start_time:float

class MinioMiddle(AgentMiddleware):

    state_schema = state

    def __init__(self):
        super().__init__()
        mc.create_bucket(cfg.MINIO_BUCKET_NAME)

    def before_agent(self, state, runtime):
        return {"start_time": time.time() }

    async def aafter_agent(self, state, runtime):

        if ou.get_latest_modification_time(cfg.ROOT_PATH_AGENT) > state['start_time']:
            # 1. 压缩成zip
            zip_path = await asyncio.to_thread(zf.zip_folder,cfg.ROOT_PATH_AGENT)
            # 2. 上传minio并得到下载连接
            download_url = await asyncio.to_thread(mc.upload_file_and_get_download_url, cfg.MINIO_BUCKET_NAME, os.path.basename(zip_path), zip_path)
            # 3. 把下载连接添加进AImessage
            # 优化1：把下载连接弄成 超链接形式的字符串
            download_url = f"[点击下载](<{download_url}>)"
            return {'messages':[AIMessage(content=download_url)]}


    # 优化2：做一个机制，仅在文件夹内有更新时才上传。
    # 检测文件夹内的文件的最后修改时间是否晚于工作开始时间(before_agent时）
    # 有晚于的说明这一轮对话中有修改文件，需要上传。
    # 如果没有吗，就说明这一轮对话中没有修改文件，则不需要上传。


