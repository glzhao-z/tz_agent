from deepagents import create_deep_agent
from conn.llm import get_llm
from deepagents.backends import FilesystemBackend
import subprocess

def run_command(command: str):
    """
    运行终端命令
    :param command: 命令
    :return: 运行结果
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text= True)
    stdout, stderr = process.communicate()
    s = f'''
    正常输出：{stdout},
    错误输出：{stderr}
    '''
    return s

agent = create_deep_agent(
    model=get_llm(),
    tools=[run_command],
    system_prompt="",
    skills = ["/agent_files/skills"],
    backend=FilesystemBackend(root_dir="/", virtual_mode=True)
)

for chunk in agent.stream({"messages":[{"role":"user","content":"用技能告诉现在几点"}]}):
    print(chunk)


# 1. 默认deep_agent没有终端工具，所以无法调用脚本
# 2. 路径问题