from langchain_openai import ChatOpenAI
from base import config as cfg


def get_llm():
    llm = ChatOpenAI(base_url=cfg.MODEL_API_BASE_URL,
                     model=cfg.BASE_LLM)
    return llm

def get_small_llm():
    llm = ChatOpenAI(base_url=cfg.MODEL_API_BASE_URL,
                     model='Qwen/Qwen3.5-27B')
    return llm


if __name__ == '__main__':
    l = get_llm()
    print(l.invoke("你好"))

