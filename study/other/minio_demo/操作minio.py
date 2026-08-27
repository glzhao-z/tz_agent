# 该代码仅为了解Python操作Minio所用，与项目无关
from minio import Minio

client = Minio(
    "localhost:9000", # url
    access_key="minio", # 账户
    secret_key="minio123", # 密码
    secure=False # 目前无https域名，所以安全设置为false
)

# 创建桶
def create_bucket(bucket_name):
    if not client.bucket_exists(bucket_name): # 如果桶不存在
        client.make_bucket(bucket_name) # 创建桶

# 上传文件
def upload_file(bucket_name, object_name, file_path):
    """
    上传文件
    :param bucket_name: 桶名
    :param object_name: 对象名(minio端的)
    :param file_path: 文件路径(本地的)
    """
    client.fput_object(bucket_name, object_name,file_path)


# 下载文件
def download_file(bucket_name, object_name, file_path):
    """
    下载文件
    :param bucket_name: 桶名
    :param object_name: 对象名(minio端的)
    :param file_path: 文件路径(本地的)
    """
    client.fget_object(bucket_name, object_name, file_path)


# 删除文件
def delete_file(bucket_name, object_name):
    """
    删除文件
    :param bucket_name: 桶名
    :param object_name: 对象名(minio端的)
    """
    client.remove_object(bucket_name, object_name)

# 得到下载链接
def get_download_object(bucket_name,object_name):
    url = client.presigned_get_object(bucket_name, object_name)
    return url

