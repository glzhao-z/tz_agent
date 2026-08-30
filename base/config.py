import os
from dotenv import load_dotenv # 导入load_dotnev(可有可无)
load_dotenv()  # 默认加载启动时当前目录下的 .env 文件 (可有可无)

ROOT_PATH_AGENT = os.path.normpath('/agent_files') # 默认代理文件存储路径
USER_UPLOAD_PATH = 'user_upload' # 用户上传文件存储路径
GENERATE_IMAGE_DIR = 'generate_image' # 生成图像文件存储路径

BASE_LLM = os.getenv("BASE_LLM") # 从环境变量中获取模型
MODEL_API_BASE_URL = os.getenv("MODEL_API_BASE_URL") # 从环境变量中获取base_url
BASE_VLM = os.getenv("BASE_VLM") # 从环境变量中获取基础VLM
IMAGE_MODEL = os.getenv("IMAGE_MODEL") # 从环境变量中获取图像模型

LOG_DIR = os.path.dirname(__file__) # 当前脚本所在目录
NEED_CONSOLE_LOG = False # 日志是否打印到控制台

if os.getenv("HOST_IP") and os.getenv("MINIO_PORT"):
    MINIO_ENDPOINT = os.getenv("HOST_IP") + ':' + os.getenv("MINIO_PORT") # 获取MinIO端点
else:
    MINIO_ENDPOINT = "localhost:9000"

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

MINIO_BUCKET_NAME = 'agent-files'

TAVILY_SEARCH_KEY = os.getenv('TAVILY_SEARCH_KEY')