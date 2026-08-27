
from langchain.agents.middleware import AgentState,AgentMiddleware
from langchain.agents.middleware.types import StateT
from langchain.messages import ToolMessage
from utils.doc_utils import zip_files as zf
from base import config as cfg


class MinioMiddle(AgentMiddleware):

    def after_agent(self, state, runtime):
        # 1. 压缩成zip
        zip_path = zf.zip_folder(cfg.ROOT_PATH_AGENT)
        # 2. 上传minio

        # 3. 得到下载连接

        # 4. 把下载连接添加进AImessage