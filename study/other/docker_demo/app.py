import fastapi

app = fastapi.FastAPI()

@app.get("/hello")
def read_root():
    return "hello world"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
任务：将该程序以docker的形式部署
1. 先搞出镜像。

2. 再通过镜像实例化容器。

3. 运行容器。
'''