from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.messages import AIMessage
from utils.doc_utils import zip_files as zf
from base import config as cfg
from conn import minio_conn as mc
import asyncio
import os

class MinioMiddle(AgentMiddleware):

    def __init__(self):
        super().__init__()
        mc.create_bucket(cfg.MINIO_BUCKET_NAME)

    async def aafter_agent(self, state, runtime):
        # 1. 压缩成zip
        zip_path = await asyncio.to_thread(zf.zip_folder,cfg.ROOT_PATH_AGENT)
        # 2. 上传minio并得到下载连接
        download_url = await asyncio.to_thread(mc.upload_file_and_get_download_url, cfg.MINIO_BUCKET_NAME, os.path.basename(zip_path), zip_path)
        # 3. 把下载连接添加进AImessage
        # 优化1：把下载连接弄成 超链接形式的字符串
        download_url = f"[点击下载](<{download_url}>)"
        return {'messages':[AIMessage(content=download_url)]}


    # 优化2：做一个机制，仅在文件夹内有更新时才上传。