"""
main.py
====================================
O módulo principal do projeto
"""
from markov import MarkovNode


def requestNode(node: str, nodeList, nodeData):
    """
    Função que cria um nó do grafo de Markov.
    """
    if node in nodeList:
        print(nodeList[node])
        return nodeList[node]
    return MarkovNode(
        node,
        nodeData[node]["probP"],
        nodeData[node]["probQ"],
        requestNode(nodeData[node]["nodeP"], nodeList, nodeData),
        requestNode(nodeData[node]["nodeQ"], nodeList, nodeData),
        nodeList,
    )


def main():
    data = {
        "A": {"probP": 0.1, "probQ": 0.2, "nodeP": "B", "nodeQ": "C"},
        "B": {"probP": 0.3, "probQ": 0.4, "nodeP": "D", "nodeQ": "E"},
        "C": {"probP": 0.5, "probQ": 0.6, "nodeP": "F", "nodeQ": "G"},
    }
    nodeList = {}
    for node in data:
        nodeList[node["name"]] = MarkovNode(
            node["name"],
            node["probP"],
            node["probQ"],
            requestNode(node["nodeP"], nodeList, data),
            requestNode(node["nodeQ"], nodeList, data),
            nodeList,
        )
    print(nodeList)
    print("All ok!")
    pass


if __name__ == "__main__":
    main()
