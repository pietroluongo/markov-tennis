"""
main.py
====================================
O módulo principal do projeto
"""
import networkx as nx
import matplotlib.pyplot as plt
import csv
from pprint import pprint
from markov import MarkovGraph, MarkovNode
from gui import MainWindow
from PyQt5.QtWidgets import QApplication
from typing import Type
import os
import json
from time import time, strftime


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


def drawUI():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


def simulateGame():
    # simulate six or seven sets
    pass


def getSeedFromTime():
    return round(time() * 1000)


class TennisGame:
    def __init__(self, set: Type[MarkovGraph]):
        self._scoreP = 0
        self._scoreQ = 0
        self._matches = []
        self._winner = None
        self._set = set
        self._results = {}
        self._gameResults = []

    def simulate(self):
        while True:
            self._set.simulateGame()
            winner = self._set.getWinner()
            if winner == "p":
                self._scoreP += 1
            else:
                self._scoreQ += 1
            print("current score: {} - {}".format(self._scoreP, self._scoreQ))
            self._gameResults.append(self._set.getResults())
            self._set.reset(getSeedFromTime())
            if self._scoreP >= 6 and self._scoreP >= self._scoreQ + 2:
                break
            if self._scoreQ >= 6 and self._scoreQ >= self._scoreP + 2:
                break

        if self._scoreP > self._scoreQ:
            self._winner = "p"
        else:
            self._winner = "q"

    def getJSON(self):
        return {
            "data": self._gameResults,
            "gameResult": {
                "score": {
                    "p": self._scoreP,
                    "q": self._scoreQ,
                },
                "winner": "{}".format(self._winner),
            },
        }

    def dumpResultsToFile(self):
        currentTime = strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists(os.path.join("results", "games")):
            os.mkdir(os.path.join("results", "games"))

        with open(
            os.path.join("results", "games", "{}.json".format(currentTime)), "w"
        ) as outputFile:
            outputFile.write(self.getJSON().__str__())


def simulateMatch():
    # simulate
    pass


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
    initialNode = MarkovNode.getNodeById("0-0")
    simTime = getSeedFromTime()
    print("Simulating game with seed {}".format(simTime))
    graph = MarkovGraph(initialNode, simTime)
    # graph.simulateGame(True)
    game = TennisGame(graph)
    game.simulate()
    game.dumpResultsToFile()
    pass


if __name__ == "__main__":
    main()
