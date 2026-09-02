from deepagents import create_deep_agent
from conn.llm import get_llm
from base import config as cfg
from content.mytools import globle_tools as gt,read_doc_tools,write_doc_tools
from content.mytools import vlm_tool,gen_image
from content.mcps import traliy_search,excel_mcp
from content.middleware import file_middle,minio_middle,rate_limit_middle
from deepagents.backends import FilesystemBackend
from content.subagents import excel_agent


# 接入skill需求1
# 1.1 如果把skill-creator放于agent工作目录中
# 启动项目时，复制代码中的skill-creator文件夹到agent工作目录中
# 1. 启动项目时直接复制，或者before_agent
# 2. 做一个文件夹复制的工具脚本


# 1.2 如何确保skill-creator产生的技能自动出现于agent工作目录中



class AllAgent():

    def __init__(self):

        system_prompt = f"""
        你是个功能强大的助手，
        {'做excel用excel-agent子代理。' if cfg.USE_EXCEL else ''}
        {cfg.USER_UPLOAD_PATH}文件夹是用户上传文件的文件夹, 不要在这个文件夹下创建新文件。
        读取word,pdf,ppt,excel等文件优先使用get_file_content工具,
        如果要写word或者pdf之类的可以先写md，然后通过convert_file工具转换,
        如果要做图文，也是先做md, 然后通过convert_file工具转场成pdf, 要特别注意图片引用路径
        如果要搜新闻，用get_current_time工具确认一下当前的日子.
        """

        self.agent  = create_deep_agent(model=get_llm(),#模型
                     tools=self.get_tools(),#工具列表
                     middleware=self.get_middles(),
                     system_prompt=system_prompt,
                     skills=[cfg.SKILLS_DIR],
                     subagents=self.get_subagents(),
                     backend=FilesystemBackend(root_dir=cfg.ROOT_PATH_AGENT,virtual_mode=True))#系统提示词

    def get_subagents(self):
        if cfg.USE_EXCEL:
            return [excel_agent.get_agent()]
        else:
            return []

    def get_middles(self):
        middles = [file_middle.FileMiddle(),rate_limit_middle.anti_rate_limit]
        if cfg.USE_MINIO:
            middles.append(minio_middle.MinioMiddle())
        return middles


    def get_tools(self):
        return [#gt.run_command,
                gt.get_current_time,
                read_doc_tools.get_file_content,
                write_doc_tools.convert_file,
                vlm_tool.read_image,
                gen_image.generate_image,
                ] + traliy_search.get_tools()

if __name__ == '__main__':
    from utils.langchain_utils import stream_util as su
    agent = AllAgent().agent

    while 1:
        user_input = input("请输入你的问题：")
        if user_input == "exit":
            break
        su.steam_both(agent,user_input)