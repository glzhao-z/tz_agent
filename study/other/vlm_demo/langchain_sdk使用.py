from langchain_openai import ChatOpenAI
from base import config as cfg
from utils.doc_utils import base64_utils as bu
from langchain.messages import HumanMessage

def get_vlm():
    vlm = ChatOpenAI(base_url=cfg.MODEL_API_BASE_URL,
                     model='moonshotai/Kimi-K2.7-Code',
                    )
    return vlm

m = HumanMessage(content=[
                {"type": "text", "text": "描述这张图片"},
                {"type": "image_url", "image_url": {"url": bu.get_base64_uri('guanyu.jpg')}}
            ])
vlm = get_vlm()
response = vlm.invoke([m])

print(response)