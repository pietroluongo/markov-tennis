"""
main.py
====================================
O módulo principal do projeto
"""
import networkx as nx
import matplotlib.pyplot as plt
import csv
from pprint import pprint
from markov import MarkovNode


# data = {
#     "A": {"probP": 0.1, "probQ": 0.2, "nodeP": "B", "nodeQ": "C"},
#     "B": {"probP": 0.3, "probQ": 0.4, "nodeP": "D", "nodeQ": "E"},
#     "C": {"probP": 0.5, "probQ": 0.6, "nodeP": "D", "nodeQ": "E"},
#     "D": {"probP": 0.5, "probQ": 0.6, "nodeP": None, "nodeQ": None},
#     "E": {"probP": 0.5, "probQ": 0.6, "nodeP": None, "nodeQ": None},
# }


def loadData(path: str):
    data = {}
    with open(path, "r") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=",")
        lineCount = 0
        for row in csvReader:
            lineCount += 1
            if lineCount == 1:
                pass
            else:
                nodeP = None
                nodeQ = None
                if row[3] != "":
                    nodeP = row[3]
                if row[4] != "":
                    nodeQ = row[4]
                data[row[0]] = {
                    "probP": row[1],
                    "probQ": row[2],
                    "nodeP": nodeP,
                    "nodeQ": nodeQ,
                }
    csvFile.close()
    return data


def drawNodes():
    graph = nx.DiGraph()
    drawNodeData = []
    for node in MarkovNode.getNodes():
        if node == None:
            return []
        if node._nodeP != None:
            drawNodeData.append(
                (node.getName(), node._nodeP.getName(), {"weight": node.getProbP()})
            )
        if node._nodeQ != None:
            drawNodeData.append(
                (node.getName(), node._nodeQ.getName(), {"weight": node.getProbQ()})
            )
    print(drawNodeData)
    graph.add_edges_from(drawNodeData)
    nx.draw_networkx_edge_labels(graph, pos=nx.planar_layout(graph))
    nx.draw(graph, pos=nx.planar_layout(graph), with_labels=True)
    plt.show()
    return


def main():
    data = loadData("tennis/stateList.csv")
    for key in data:
        MarkovNode(
            key,
            data[key]["probP"],
            data[key]["probQ"],
            data[key]["nodeP"],
            data[key]["nodeQ"],
        )
    MarkovNode.populateNodes()
    drawNodes()
    pass


if __name__ == "__main__":
    main()
