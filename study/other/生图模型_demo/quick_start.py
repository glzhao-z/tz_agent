import requests
from base import config
import os
import httpx

def generate_image(prompt,out_path):
    url = "https://api.siliconflow.cn/v1/images/generations"
    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": prompt,
        "image_size": "1024x1024", # 图像大小
        "batch_size": 1, # 批处理大小
        "num_inference_steps": 20, # 推理步数
        "guidance_scale": 7.5, # 指导尺度
        #"image": "https://inews.gtimg.com/om_bt/Os3eJ8u3SgB3Kd-zrRRhgfR5hUvdwcVPKUTNO6O7sZfUwAA/641"
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

generate_image("二次元狗","dog.png")