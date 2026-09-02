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
1.1 写Dockerfile(定义这个镜像所需要的环境)
假设要运行一个fastapi程序，至少需要。
1. 操作系统
2. python
3. fastapi 
1.2 运行docker build命令
docker build -t hellohello .

docker run -d -p 8000:8000 hellohello . 

2. 再通过镜像实例化容器。

3. 运行容器。

key: value  # 键值对
list: # 列表
  - item1
  - item2
nested: # 嵌套字典
  child: value

{
    'key':'value',
    'list':['item1','item2'],
    'nested':{'child':'value'}

}
'''