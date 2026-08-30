import os.path
import uuid
from conn import gen_img
from utils.doc_utils.download_utils import download_file
from base import config as cfg

def generate_image(prompt,image_size,ref_image_path=None):
    """
    生成图片
    :param prompt:
    :param image_size:
    :param ref_image_path:
    :return:
    """
    url = gen_img.generate_image(prompt,image_size,ref_image_path)
    # 当我们需要一个不重复的字符串时，就可以使用uuid
    out_path = os.path.join(cfg.GENERATE_IMAGE_DIR, uuid.uuid4().hex + '.png')
    # 下载图片
    download_file(url,out_path)
    return out_path