"""
main.py
====================================
O módulo principal do projeto
"""
import networkx as nx
import matplotlib.pyplot as plt
import csv

from markov import MarkovGraph, MarkovNode
from gui import MainWindow
from PyQt5.QtWidgets import QApplication
from typing import Type
import os
from time import time, strftime


def loadData(path: str):
    """
    Carrega os dados de geração do grafo de Markov a partir de um arquivo CSV.
    A ordem de colunas do arquivo deve ser a seguinte:
        - nodeName (string): identificador do nó
        - p (float): probabilidade de vitória de P
        - q (float): probabilidade de vitória de Q
        - pWinsNode (string): identificador do nó associado à vitória de P
        - qWinsNode (string): identificador do nó associado à vitória de Q
    """
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
    """
    Desenha uma representação gráfica do grafo de Markov. Usado apenas para fins de depuração.
    """
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
    """
    Desenha a interface gráfica do programa. Não implementado.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


def getSeedFromTime(iter: int):
    """
    Função auxiliar usada para obter um seed para o gerador de números aleatórios a partir
    do tempo atual.

    Returns:
        (int) tempo atual em milissegundos
    """
    return round(time() * 1000 * iter)


class TennisSet:
    """
    Classe que representa um Set (conjunto de games) de Tênis.
    """

    def __init__(self, game: Type[MarkovGraph]):
        """
        Inicializa o jogo.

        Args:
            set (`tennis.markov.MarkovGraph`): Conjunto de informações que representam um set.
                Já deve estar completamente inicializado.
        """
        self._scoreP = 0
        self._scoreQ = 0
        self._matches = []
        self._winner = None
        self._game = game
        self._results = {}
        self._gameResults = []
        self._shouldRun = True

    def simulate(self):
        """
        Simula um game - ou seja, um conjunto de sets. Os jogos são simulados até que um dos
        jogadores atinja ao menos seis sets E uma diferença de ao menos dois sets em relação ao
        seu adversário. O valor da variável de instância `_winner` indica o vencedor do game ao
        fim da execução do método, e pode ser acessada via `getWinner`
        """
        while self._shouldRun:
            self._game.simulateGame()
            winner = self._game.getWinner()
            if winner == "p":
                self._scoreP += 1
            else:
                self._scoreQ += 1
            self._gameResults.append(self._game.getResults())
            self._game.reset(getSeedFromTime(self._scoreP + self._scoreQ))
            if self._scoreP == 2:
                self._winner = "p"
                self._shouldRun = False

            if self._scoreQ == 2:
                self._winner = "q"
                self._shouldRun = False
        print(
            "{} won the set by {}-{}".format(self._winner, self._scoreP, self._scoreQ)
        )

    def getWinner(self):
        """
        Retorna o vencedor do game atual.

        Returns:
            (str): "p", se o vencedor for P, e "q", se o vencedor for Q
        """
        return self._winner

    def getJSON(self):
        """
        Retorna uma representação em JSON dos dados do game atual.

        Formato:

            O objeto retornado segue o seguinte formato:

                {
                    data: vetor de dados retornados dos sets - ver comentário abaixo,
                    gameResult: {
                        score: {
                            p (int): pontuação de P,
                            q (int): pontuação de Q
                        }
                    },
                    winner (str): "p" se o vencedor for P, e "q" se o vencedor for Q
                }
            A estrutura de `data` é descrita em detalhes em `tennis.markov.MarkovGraph.getResults`.
        """
        return {
            "data": self._gameResults,
            "setResult": {
                "score": {
                    "p": self._scoreP,
                    "q": self._scoreQ,
                },
                "winner": "{}".format(self._winner),
            },
        }

    def dumpResultsToFile(self):
        """
        Escreve os dados do game atual em um arquivo JSON, no caminho `/results/sets/data-hora-do-jogo.json`.
        A formatação do arquivo é descrita em `getJSON`.
        """
        currentTime = strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists(os.path.join("results", "sets")):
            os.mkdir(os.path.join("results", "sets"))

        with open(
            os.path.join("results", "sets", "{}.json".format(currentTime)), "w"
        ) as outputFile:
            outputFile.write(self.getJSON().__str__())

    def reset(self):
        self._scoreP = 0
        self._scoreQ = 0
        self._matches = []
        self._winner = None
        self._gameResults = []
        self._shouldRun = True


class TennisMatch:
    """
    Simula uma partida - ou seja, um conjunto de sets.
    """

    idx = 0

    def __init__(self, graph: Type[MarkovGraph]):
        """
        Inicializa a partida.

        Args:
            graph (`tennis.markov.MarkovGraph`): Conjunto de informações que representam um ponto.
                Já deve estar completamente inicializado.
        """
        self._winner = None
        self._sets = []
        self._set = TennisSet(graph)
        self._results = {}
        self._scoreP = 0
        self._scoreQ = 0
        self._graph = graph

    def simulate(self, shouldDumpToFile=False):
        """
        Simula uma partida - ou seja, um conjunto de sets. Os jogos são simulados até que um dos
        jogadores atinja ao menos dois sets. O valor da variável de instância `_winner` indica o
        vencedor do game ao fim da execução do método, e pode ser acessada via `getWinner`
        """
        while True:
            self._set.simulate()
            winner = self._set.getWinner()
            if winner == "p":
                self._scoreP += 1
            else:
                self._scoreQ += 1
            print(
                "{} won match. current match score: {} - {}".format(
                    winner, self._scoreP, self._scoreQ
                )
            )
            self._sets.append(self._set.getJSON())
            self._set.reset()
            if self._scoreP == 2:
                self._winner = "p"
                break
            if self._scoreQ == 2:
                self._winner = "q"
                break
        if shouldDumpToFile:
            self.dumpToFile()

    def toJSON(self):
        """
        Retorna uma representação em JSON dos dados da partida atual.

        Formato:

            O objeto retornado segue o seguinte formato:

                {
                    data: vetor de dados retornados dos sets - ver comentário abaixo,
                    matchResult: {
                        score: {
                            p (int): pontuação de P,
                            q (int): pontuação de Q
                        }
                    },
                    winner (str): "p" se o vencedor for P, e "q" se o vencedor for Q
                }
            A estrutura de `data` é descrita em detalhes em `TennisSet.getJSON`.
        """
        return {
            "seed": self._graph.getSeed(),
            "data": self._sets,
            "matchResult": {
                "score": {
                    "p": self._scoreP,
                    "q": self._scoreQ,
                },
                "winner": "{}".format(self._winner),
            },
        }

    def dumpToFile(self):
        """
        Escreve os dados da partida atual em um arquivo JSON, no caminho `/results/matches/data-hora-do-jogo.json`.
        A formatação do arquivo é descrita em `toJSON`.
        """
        currentTime = strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists(os.path.join("results", "matches")):
            os.mkdir(os.path.join("results", "matches"))

        with open(
            os.path.join(
                "results", "matches", "{}-{}.json".format(currentTime, TennisMatch.idx)
            ),
            "w",
        ) as outputFile:
            outputFile.write(self.toJSON().__str__())
            TennisMatch.idx += 1

    def getWinner(self):
        """
        Retorna o vencedor do game atual.

        Returns:
            (str): "p", se o vencedor for P, e "q", se o vencedor for Q
        """
        return self._winner


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
    for i in range(0, 40):
        simTime = getSeedFromTime(i + 1)
        print("Simulating game with seed {}".format(simTime))
        graph = MarkovGraph(initialNode, simTime)
        match = TennisMatch(graph)
        match.simulate(True)

    pass


if __name__ == "__main__":
    main()
