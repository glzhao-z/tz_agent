from langchain_openai import ChatOpenAI
# 加载环境变量
import dotenv
dotenv.load_dotenv()

def get_llm():
    llm = ChatOpenAI(base_url='https://api.siliconflow.cn/v1',
                     model='Qwen/Qwen3.5-27B')
                     #model='Qwen/Qwen3-Next-80B-A3B-Instruct')
    return llm





if __name__ == '__main__':
    model = get_llm()

    system_prompt = "你是小明，每次回答用户问题都告诉他你是小明"
    messages = [{"role": "user", "content": "你好"}]
    new_messages = [{"role": "system", "content": system_prompt}] + messages
    r = model.invoke(new_messages)

    print(r)
    print(type(r)) # AIMessage


