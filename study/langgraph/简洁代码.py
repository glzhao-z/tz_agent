import os

'''
#宏观
图(graph)工作流，节点与边.
(图片figure)
节点：负责工作
边：负责连接

状态: 用于在节点间传递信息的载体，程序里本质上是一个字典,实际上是一个字典模板
'''
from langgraph.graph import StateGraph
from langgraph.graph import START,END # 每个图工作都需要有开始和结束节点


# 状态
from typing_extensions import TypedDict
class State(TypedDict):
    key1: str
    key2: int

# 节点
# 要把一个函数作为langgraph的节点，则有一定约束。
# 函数的输入参数必须是State类型。
def node1(state:State):
    print('node1')
    print(state)

def node2(state:State):
    print('node2')
# 先实例化一个图, 传入状态模板State
graph = StateGraph(State)
graph.add_node("n1", node1) # 添加节点,给节点取个名字，第二个参数是节点函数
graph.add_node("n2", node2)
# 边
graph.add_edge(START, "n1")
graph.add_edge("n1", "n2")
graph.add_edge("n2", END)
# 编译图
g = graph.compile()

# 5.保存figure(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "n1.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 执行， 执行时传入state的初始值
a = g.invoke({'key1':'asda'})
print(a)