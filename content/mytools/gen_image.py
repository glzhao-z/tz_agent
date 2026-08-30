from conn import gen_img
from utils.doc_utils.download_utils import download_file


def generate_image(prompt,image_size,ref_image_path=None,out_path=None):
    """
    生成图片
    :param prompt:
    :param image_size:
    :param ref_image_path:
    :param out_path:
    :return:
    """
    url = gen_img.generate_image(prompt,image_size,ref_image_path)
    # 下载图片
    download_file(url,out_path)