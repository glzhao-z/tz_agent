import requests
from base import config as cfg
import os
from utils.doc_utils import base64_utils as bu

def generate_image(prompt,image_size,ref_image_path=None):
    url = "https://api.siliconflow.cn/v1/images/generations"
    payload = {
        "model": cfg.IMAGE_MODEL,
        "prompt": prompt,
        "image_size": image_size, # 图像大小
        "batch_size": 1, # 批处理大小
        "num_inference_steps": 20, # 推理步数
        "guidance_scale": 7.5, # 指导尺度
    }
    if ref_image_path: # 如果有参考图像路径
        payload["image"] = bu.get_base64_uri(ref_image_path) # 添加参考图像

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    d = response.json()
    url = d['images'][0]['url']
    return url

