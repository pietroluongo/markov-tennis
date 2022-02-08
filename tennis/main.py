"""
main.py
====================================
O módulo principal do projeto
"""
import networkx as nx
import matplotlib.pyplot as plt
from markov import MarkovNode


def main():
    data = {
        "A": {"probP": 0.1, "probQ": 0.2, "nodeP": "B", "nodeQ": "C"},
        "B": {"probP": 0.3, "probQ": 0.4, "nodeP": "D", "nodeQ": "E"},
        "C": {"probP": 0.5, "probQ": 0.6, "nodeP": "D", "nodeQ": "E"},
        "D": {"probP": 0.5, "probQ": 0.6, "nodeP": None, "nodeQ": None},
        "E": {"probP": 0.5, "probQ": 0.6, "nodeP": None, "nodeQ": None},
    }
    for key in data:
        nodeData = data[key]
        print("building", nodeData, "w/ key", key)
        MarkovNode.setNodeData(data)
        MarkovNode._nodes[key] = MarkovNode.requestNode(key)
    graph = nx.DiGraph()
    # drawNodeData = list(map(apply, MarkovNode._nodes.values()))
    drawNodeData = []
    for node in MarkovNode._nodes.values():
        if node == None:
            return []
        if node._nodeP != None:
            drawNodeData.append(
                (node._name, node._nodeP._name, {"weight": node._probP})
            )
        if node._nodeQ != None:
            drawNodeData.append(
                (node._name, node._nodeQ._name, {"weight": node._probQ})
            )
    print(drawNodeData)
    graph.add_edges_from(drawNodeData)
    nx.draw_networkx_edge_labels(graph, pos=nx.planar_layout(graph))
    nx.draw(graph, pos=nx.planar_layout(graph), with_labels=True)
    plt.show()

    pass


if __name__ == "__main__":
    main()
