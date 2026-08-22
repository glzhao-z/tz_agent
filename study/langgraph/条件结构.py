
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


def node3(state: State):
    print('node3')


# 条件函数(接收state,返回字符串)
def conditional_func(state:State):
    if state['key2'] > 1:
        return '1'
    elif state['key2']>0:
        return '0'
    else:
        return '222'


# 先实例化一个图, 传入状态模板State
graph = StateGraph(State)
graph.add_node("n1", node1) # 添加节点,给节点取个名字，第二个参数是节点函数
graph.add_node("n2", node2)
graph.add_node("n3", node3)
# 边
graph.add_edge(START, "n1")
graph.add_edge(['n2','n3'], END)



path_map = {
    '1': 'n2',
    '0': 'n3',
    '222':END
}
# 条件边
graph.add_conditional_edges(
    source='n1',# 源节点
    path=conditional_func, # 条件函数
    path_map=path_map #路径映射字典
)


# 编译图
g = graph.compile()

# 5.保存figure(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "n1.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 执行， 执行时传入state的初始值
a = g.invoke({'key2':0})
print(a)