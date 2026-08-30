import os.path
import uuid
from conn import gen_img
from utils.doc_utils.download_utils import download_file
from base import config as cfg

def generate_image(prompt,image_size,ref_image_path=None):
    """
    生图工具，可以文生成图，也可图生图，图生图时要传ref_image_path(参考图路径)
    :param prompt: 生图提示提
    :param image_size: 图片尺寸，枚举值：
           "1024x1024" (1:1)
           "960x1280" (3:4)
           "768x1024" (3:4)
           "720x1440" (1:2)
           "720x1280" (9:16)
    :param ref_image_path: # 参考图路径
    :return: 生成的图片路径
    """
    url = gen_img.generate_image(prompt,image_size,ref_image_path)
    image_dir = os.path.join(cfg.ROOT_PATH_AGENT,cfg.GENERATE_IMAGE_DIR)
    os.makedirs(image_dir, exist_ok=True)

    # 当我们需要一个不重复的字符串时，就可以使用uuid
    out_path = os.path.join(image_dir, uuid.uuid4().hex + '.png')
    # 下载图片
    download_file(url,out_path)
    return out_path