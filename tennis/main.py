"""
main.py
====================================
O módulo principal do projeto
"""
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
    print("nodes are ", MarkovNode._nodes)
    pass


if __name__ == "__main__":
    main()
