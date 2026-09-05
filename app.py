import fastapi

app = fastapi.FastAPI()

@app.get("/hello")
def read_root():
    return "hello world"




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

