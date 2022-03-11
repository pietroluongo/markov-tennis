"""
main.py
====================================
O módulo principal do projeto
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv

from markov import MarkovGraph, MarkovNode
from gui import MainWindow
from PyQt5.QtWidgets import QApplication
from typing import Type
import os
from time import time, strftime
import argparse
import json


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


def mean(list):
    return sum(list) / len(list)


def dp(list):
    iMean = mean(list)
    return (sum([(x - iMean) ** 2 for x in list]) / len(list)) ** 0.5


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
            if self._scoreP > self._scoreQ + 2 and self._scoreP >= 6:
                self._winner = "p"
                self._shouldRun = False

            if self._scoreQ > self._scoreP + 2 and self._scoreQ >= 6:
                self._winner = "q"
                self._shouldRun = False

            if self._scoreQ == 7:
                self._winner = "p"
                self._shouldRun = False

            if self._scoreP == 7:
                self._winner = "q"
                self._shouldRun = False

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
            "setData": self._gameResults,
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
            "matchData": self._sets,
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
            outputFile.write(json.dumps(self.toJSON()))
            TennisMatch.idx += 1

    def getWinner(self):
        """
        Retorna o vencedor do game atual.

        Returns:
            (str): "p", se o vencedor for P, e "q", se o vencedor for Q
        """
        return self._winner


def main(shouldSimulate=False, shouldAnalyze=False, datasetPath=None):
    """
    Função principal do programa.

    Args:
        shouldSimulate (bool): Se True, simula uma partida.
        shouldAnalyze (bool): Se True, analisa os dados de um dataset.
        datasetPath (str): Caminho para o dataset a ser analisado.
    """
    if shouldSimulate:
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
        for i in range(0, 300):
            simTime = getSeedFromTime(i + 1)
            print("Simulating game with seed {}".format(simTime))
            graph = MarkovGraph(initialNode, simTime)
            match = TennisMatch(graph)
            match.simulate(True)
    if shouldAnalyze:
        datasetFiles = os.listdir(datasetPath)
        dataset = []
        for file in datasetFiles:
            with open(os.path.join(datasetPath, file), "r") as inputFile:
                data = json.loads(inputFile.read())
                dataset.append(data)

        rands = []
        setCount = 0
        setCountPerGameForP = []
        setCountPerGameForQ = []
        gameCount = 0
        gameCountForP = []
        gameCountForQ = []
        pointCount = 0
        pointCountForP = []
        pointCountForQ = []
        pWinsMatch = list(filter(lambda x: x["matchResult"]["winner"] == "p", dataset))

        splitGames = []

        for i in range(0, len(dataset), 3):
            splitGames.append(dataset[i : i + 3])

        print(splitGames[0][0]["matchResult"]["winner"])
        pGroupWinsData = []
        qGroupWinsData = []
        for threeGames in splitGames:
            p = 0
            q = 0
            for singleGame in threeGames:
                if singleGame["matchResult"]["winner"] == "p":
                    p += 1
                else:
                    q += 1
            pGroupWinsData.append(p)
            qGroupWinsData.append(q)

        print("P wins mean = {}".format(mean(pGroupWinsData)))
        print("Q wins mean = {}".format(mean(qGroupWinsData)))

        print("P wins dp = {}".format(dp(pGroupWinsData)))
        print("Q wins dp = {}".format(dp(qGroupWinsData)))

        for match in dataset:
            pSet = 0
            qSet = 0
            pGame = 0
            qGame = 0
            pPoint = 0
            qPoint = 0
            for setData in match["matchData"]:
                setCount += 1
                if setData["setResult"]["winner"] == "p":
                    pSet += 1
                else:
                    qSet += 1
                for gameData in setData["setData"]:
                    gameCount += 1
                    if gameData["gameWinner"] == "p":
                        pGame += 1
                    else:
                        qGame += 1
                    pointCount += len(gameData["gameData"])
                    for point in gameData["gameData"]:
                        if point["scorer"] == "p":
                            pPoint += 1
                        else:
                            qPoint += 1
                        rands.append(point["resultValue"])
            setCountPerGameForP.append(pSet)
            setCountPerGameForQ.append(qSet)
            gameCountForP.append(pGame)
            gameCountForQ.append(qGame)
            pointCountForP.append(pPoint)
            pointCountForQ.append(qPoint)

        print("media de pontos de P por partida = {}".format(mean(pointCountForP)))
        print("media de pontos de Q por partida = {}".format(mean(pointCountForQ)))

        print("dp de pontos de P por partida = {}".format(dp(pointCountForP)))
        print("dp de pontos de Q por partida = {}".format(dp(pointCountForQ)))

        print("media de sets de P por partida = {}".format(mean(setCountPerGameForP)))
        print("media de sets de Q por partida = {}".format(mean(setCountPerGameForQ)))

        print("dp de sets de P por partida = {}".format(dp(setCountPerGameForP)))
        print("dp de sets de Q por partida = {}".format(dp(setCountPerGameForQ)))

        print("media de games de P por partida = {}".format(mean(gameCountForP)))
        print("media de games de Q por partida = {}".format(mean(gameCountForQ)))

        print("dp de games de P por partida = {}".format(dp(gameCountForP)))
        print("dp de games de Q por partida = {}".format(dp(gameCountForQ)))

        print("total de sets: {}".format(setCount))
        print("total de jogos: {}".format(gameCount))
        print("total de pontos: {}".format(pointCount))

        med = sum(rands) / len(rands)
        print("media dos numeros sorteados: {}".format(med))
        print(
            "p ganha em média {} de {} partidas, {}%".format(
                len(pWinsMatch), len(dataset), len(pWinsMatch) / len(dataset) * 100
            )
        )
        randomValsDP = (
            sum(list(map(lambda x: (x - med) ** 2, rands))) / len(rands)
        ) ** 0.5
        print("desvio padrão dos numeros sorteados: {}".format(randomValsDP))
        print("em média, cada partida tem {} pontos".format(pointCount / setCount))
        print("em média, cada jogo tem {} pontos".format(pointCount / gameCount))
        print("em média, cada set tem {} jogos".format(gameCount / setCount))
        fig1, ax1 = plt.subplots(1, 2)
        ax1[0].set_title("Distribuição dos pontos de P ao longo das simulações")
        ax1[1].set_title("Distribuição dos pontos de Q ao longo das simulações")
        ax1[0].boxplot(pointCountForP, boxprops=dict(color="C0"))
        ax1[1].boxplot(pointCountForQ, boxprops=dict(color="C2"))
        plt.show()

        fig2, ax2 = plt.subplots(1, 2)
        ax2[0].set_title("Distribuição dos sets de P ao longo das simulações")
        ax2[1].set_title("Distribuição dos sets de Q ao longo das simulações")
        ax2[0].boxplot(setCountPerGameForP, boxprops=dict(color="C0"))
        ax2[1].boxplot(setCountPerGameForQ, boxprops=dict(color="C2"))
        plt.show()

        fig3, ax3 = plt.subplots(1, 2)
        ax3[0].set_title("Distribuição dos games de P ao longo das simulações")
        ax3[1].set_title("Distribuição dos games de Q ao longo das simulações")
        ax3[0].boxplot(gameCountForP, boxprops=dict(color="C0"))
        ax3[1].boxplot(gameCountForQ, boxprops=dict(color="C2"))
        plt.show()


parser = argparse.ArgumentParser(
    description="Simulação de partidas de tênis usando Cadeias de Markov"
)
parser.add_argument(
    "--simulate",
    "-S",
    action="store_true",
    help="Simula uma partida de tênis",
)
parser.add_argument(
    "--analyze",
    "-A",
    action="store_true",
    help="Analisa os resultados de uma partida armazenados em um dataset",
)
parser.add_argument("--path", "-p", help="Caminho para a pasta contendo o dataset")
args = parser.parse_args()


if __name__ == "__main__":
    if args.analyze and not args.path:
        print("É necessário informar o caminho para o dataset")
        exit(1)
    if args.analyze and args.simulate:
        print(
            "Não é possível gerar os dados e simular uma partida ao mesmo tempo. Faça a simulação primeiro e depois analise os resultados."
        )
        exit(1)
    main(args.simulate, args.analyze, args.path)
