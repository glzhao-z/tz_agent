from deepagents import create_deep_agent
from conn.llm import get_llm
from deepagents.backends import FilesystemBackend
from base import config as cfg

class AllAgent():

    def __init__(self):
        self.agent  = create_deep_agent(model=get_llm(),#模型
                     tools=[],#工具列表
                     system_prompt='你是一个助理',
                     backend=FilesystemBackend(root_dir=cfg.ROOT_PATH_AGENT,virtual_mode=True))#系统提示词


if __name__ == '__main__':
    from utils.langchain_utils import stream_util as su
    agent = AllAgent().agent

    su.steam_both(agent,'你好')