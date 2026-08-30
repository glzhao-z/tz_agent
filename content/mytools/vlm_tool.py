from conn.llm import get_vlm
from utils.doc_utils import base64_utils as bu
from langchain.messages import HumanMessage
vlm = get_vlm()

def read_image(image_path):
    """
    理解图片的工具
    :param image_path: 图片路径
    :return: 图片的理解结果，字符串格式
    """
    # 先把图片编码成base64 uri
    base64_uri = bu.get_base64_uri(image_path)
    # 调用vlm得到返回
    m = HumanMessage(content=[
        {"type": "text", "text": "描述这张图片"},
        {"type": "image_url", "image_url": {"url": base64_uri}}
    ])
    response = vlm.invoke([m])
    # 解析返回结果输出
    return response.content

if __name__ == '__main__':
    read_image(r'D:\workspace\pythonworkspace\projects\normal\all_agent_study2\study\other\vlm_demo\guanyu.jpg')