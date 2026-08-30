from mcp.server.fastmcp import FastMCP

# 1. 定义服务端基本信息
mcp = FastMCP("demo",host="127.0.0.1",port=8001)


# 2. 定义工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数相加"""
    print("正在执行加法运算...")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """两个数相乘"""
    print("正在执行乘法运算...")
    return a * b

# 3. 启动服务
if __name__ == "__main__":
    mcp.run(transport='sse')