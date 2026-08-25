


def save_graph(agent,image_path):
    graph_image = agent.get_graph().draw_mermaid_png()
    with open(image_path, "wb+") as f:
        f.write(graph_image)