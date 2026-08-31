from deepagents import create_deep_agent
from conn.llm import get_llm
from deepagents.backends import FilesystemBackend
import subprocess



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