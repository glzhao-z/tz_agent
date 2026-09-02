# 基础镜像
FROM python:3.11

# 定义镜像内的工作目录
WORKDIR /sss

# 把当前的程序代码复制到镜像内的工作目录
COPY . .

# 安装基础镜像以外并且程序可能用到的依赖
RUN pip install fastapi uvicorn

# 定义容器启动时运行的命令
CMD ["python","app.py"]
