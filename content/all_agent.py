from deepagents import create_deep_agent
from conn.llm import get_llm
from base import config as cfg
from content.mytools import globle_tools as gt,read_doc_tools,write_doc_tools
from content.mytools import vlm_tool,gen_image
from content.middleware import file_middle,minio_middle,rate_limit_middle
from deepagents.backends import FilesystemBackend

class AllAgent():

    def __init__(self):

        system_prompt = """
        你是个功能强大的助手，
        word,pdf,ppt,excel等文件优先使用get_file_content工具
        如果要写word或者pdf之类的可以先写md，然后通过convert_file工具转换
        如果要做图文，也是先做md, 然后通过convert_file工具转场成pdf
        """

        self.agent  = create_deep_agent(model=get_llm(),#模型
                     tools=self.get_tools(),#工具列表
                     middleware=self.get_middles(),
                     system_prompt=system_prompt,
                     backend=FilesystemBackend(root_dir=cfg.ROOT_PATH_AGENT,virtual_mode=True))#系统提示词

    def get_middles(self):
        return [file_middle.FileMiddle(),
                minio_middle.MinioMiddle(),
            rate_limit_middle.anti_rate_limit]


    def get_tools(self):
        return [gt.run_command,
                gt.get_current_time,
                read_doc_tools.get_file_content,
                write_doc_tools.convert_file,
                vlm_tool.read_image,
                gen_image.generate_image]

if __name__ == '__main__':
    from utils.langchain_utils import stream_util as su
    agent = AllAgent().agent

    while 1:
        user_input = input("请输入你的问题：")
        if user_input == "exit":
            break
        su.steam_both(agent,user_input)