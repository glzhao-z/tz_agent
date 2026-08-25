
from langchain.messages import HumanMessage,AIMessageChunk
from utils.general_utils.loggers import logger

# 流式打印日志
def stream_log(agent, input):
    generator = agent.stream(input={"messages": {'role': 'user', 'content': input}})
    for chunk in generator:
        logger.info(chunk)

# 流式打印tokens
def stream_print_tokens(agent, input):
    generator = agent.stream(input={"messages": {'role': 'user', 'content': input}},stream_mode="messages")
    for chunk in generator:
        content = chunk[0].content
        if content:
            print(chunk[0].content, end="", flush=True)


def steam_both(agent,user_input):
    r = agent.stream({"messages": [HumanMessage(content=user_input)]},stream_mode=["messages","updates"])
    for a in r:
        if a[0]=='updates':
            logger.info(a)
        else:
            chunk = a[1][0]
            if type(chunk)==AIMessageChunk:
                token = chunk.content
                print(token.strip(),end='', flush=True)

