from langchain_openai import ChatOpenAI

# 加载环境变量
import dotenv
dotenv.load_dotenv()


def get_llm():
    llm = ChatOpenAI(base_url='https://api.siliconflow.cn/v1',
                     model='Qwen/Qwen3.5-27B')
    return llm

