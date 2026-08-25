from deepagents import create_deep_agent
from conn.llm import get_small_llm as get_llm
from deepagents.backends import FilesystemBackend
from base import config as cfg
from content.mytools import globle_tools as gt
from content.middleware import try_middle as tm
from content.mybackend import runtime_util as ru

class AllAgent():

    def __init__(self):
        self.agent  = create_deep_agent(model=get_llm(),#模型
                     tools=[gt.run_command,gt.get_current_time],#工具列表
                     middleware=[tm.try_session],
                     system_prompt='你是一个助理',
                     backend=ru.my_backend_factory)#系统提示词


if __name__ == '__main__':
    from utils.langchain_utils import stream_util as su
    agent = AllAgent().agent

    while 1:
        user_input = input("请输入你的问题：")
        if user_input == "exit":
            break
        su.steam_both(agent,user_input)