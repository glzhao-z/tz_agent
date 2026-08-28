import requests
from dotenv import load_dotenv
load_dotenv()
import os
from utils.doc_utils import base64_utils as bu
url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY")  # 替换成你的 API key
}

data = {
    "model": "moonshotai/Kimi-K2.7-Code",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "描述这张图片"},
                {"type": "image_url", "image_url": {"url": bu.get_base64_uri('guanyu.jpg')}}
            ]
        }
    ],
    "max_tokens": 4096
}
response = requests.post(url, headers=headers, json=data)
# 打印响应
print(response.status_code)
print(response.json())