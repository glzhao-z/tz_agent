from langgraph.graph import StateGraph
from langgraph.graph import START,END # 每个图工作都需要有开始和结束节点


# 状态
from typing_extensions import TypedDict


class State(TypedDict):
    key1: str
    key2: int
    key3: int

def node1(state:State):
    # 按照langgraph的机制，这个state是全局state的浅拷贝
    # 所以对节点内部state的修改不会影响全局state
    print(state)
    state['key2']+= 1 # 经过node1, key2加1
    '''
    节点函数的返回正常情况是一个字典
    字典中的key就是对应要更新的状态的key
    '''
    return {'key2':state['key2']}

def node2(state:State):
    print(state)
    print('node2')
    # 如果要让节点更新状态中的值，则该键必须定义在状态模板中，否则会忽略，例如以下这个key4不会传递到最终状态
    return {'key1':222,'key3':333,'key4':444}

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
a = g.invoke({'key1':'22','key2':0})
print('最终输出')
print(a)