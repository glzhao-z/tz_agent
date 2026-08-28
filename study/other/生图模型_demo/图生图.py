import requests
from base import config
import os
import httpx
from utils.doc_utils import base64_utils as bu

def generate_image(prompt,out_path):
    url = "https://api.siliconflow.cn/v1/images/generations"
    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": prompt,
        "image_size": "1024x1024", # 图像大小
        "batch_size": 1, # 批处理大小
        "num_inference_steps": 50, # 推理步数
        "guidance_scale": 7.5, # 指导尺度
        "image": bu.get_base64_uri("dog.png")
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    d = response.json()
    url = d['images'][0]['url']
    with httpx.Client() as client:
        response = client.get(url)
        with open(out_path, 'wb') as f:
            f.write(response.content)

generate_image("把狗换成猫","dog2.png")