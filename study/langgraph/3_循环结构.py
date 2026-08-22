


from langgraph.graph import StateGraph
from langgraph.graph import START,END # 每个图工作都需要有开始和结束节点

'''
中心思想
1. 利用条件边制作一个跳出循环的条件
2. 当前案例即通过判断循环次数是否大于某个值来跳出循环 (在条件函数中判断)
3. 要在节点中增加 state中的count字段，用于记录循环次数
'''


# 状态
from typing_extensions import TypedDict
class State(TypedDict):
    count: int # 用于记录循环次数

# 节点
# 要把一个函数作为langgraph的节点，则有一定约束。
# 函数的输入参数必须是State类型。
def node1(state:State):
    pass

def node2(state:State):
    state['count'] += 1 # 增加循环次数
    print('count:', state['count'])
    return state

# 判断是否要跳出循环的条件
def conditional(state:State):
    if state['count'] < 5:
        return 'continue'
    else:
        return 'break'

path_map = {
    'continue': 'n2',
    'break': END
}


# 先实例化一个图, 传入状态模板State
graph = StateGraph(State)
graph.add_node("n1", node1) # 添加节点,给节点取个名字，第二个参数是节点函数
graph.add_node("n2", node2)
# 边
graph.add_edge(START, "n1")
graph.add_conditional_edges("n1", conditional, path_map)
graph.add_edge("n2", "n1")


# 编译图
g = graph.compile()

# 5.保存figure(可选)
graph_image = g.get_graph().draw_mermaid_png()
image_path = "loop.png"
with open(image_path, "wb+") as f:
    f.write(graph_image)

# 执行， 执行时传入state的初始值
a = g.invoke({'count':0})
print(a)