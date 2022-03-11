"""
main.py
====================================
O módulo principal do projeto
"""
from utils import getSeedFromTime, mean, dp
from markov import MarkovGraph, MarkovNode
from tennisClasses import TennisMatch

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv

import os
import json
import argparse


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


def mainSimulate(simulationCount: int):
    """
    Carrega os dados, constrói a cadeia de Markov e simula um jogo de tênis.

    Args:
        simulationCount (int): Quantidade de partidas a serem simuladas.

    """
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
    for i in range(0, simulationCount):
        simTime = getSeedFromTime(i + 1)
        print("Simulating game with seed {}".format(simTime))
        graph = MarkovGraph(initialNode, simTime)
        match = TennisMatch(graph)
        match.simulate(True)


def generateStats(datasetPath: str, shouldShowGraphs: bool):
    """
    Analisa os resultados de uma partida armazenados em um dataset.

    Args:
        datasetPath (str): Caminho para o dataset a ser analisado.
        shouldShowGraphs (bool): Se True, gera gráficos dos resultados.
    """
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
    randomValsDP = (sum(list(map(lambda x: (x - med) ** 2, rands))) / len(rands)) ** 0.5
    print("desvio padrão dos numeros sorteados: {}".format(randomValsDP))
    print("em média, cada partida tem {} pontos".format(pointCount / setCount))
    print("em média, cada jogo tem {} pontos".format(pointCount / gameCount))
    print("em média, cada set tem {} jogos".format(gameCount / setCount))

    if not shouldShowGraphs:
        return

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


def main(
    shouldSimulate=False,
    shouldAnalyze=False,
    datasetPath=None,
    shouldShowGraphs=False,
    simulationCount=30,
):
    """
    Função principal do programa.

    Args:
        shouldSimulate (bool): Se True, simula uma partida.
        shouldAnalyze (bool): Se True, analisa os dados de um dataset.
        datasetPath (str): Caminho para o dataset a ser analisado.]
        shouldShowGraphs (bool): Se True, mostra os gráficos gerados.
    """
    if shouldSimulate:
        mainSimulate(simulationCount)
    if shouldAnalyze:
        generateStats(datasetPath, shouldShowGraphs)


def checkArgs():
    """
    Verifica se os argumentos passados são válidos.
    """
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

    parser.add_argument(
        "--no-graphs", action="store_true", help="Não gera gráficos dos resultados"
    )

    parser.add_argument(
        "--simulation-count",
        "-C",
        type=int,
        default=30,
        help="Quantidade de partidas a serem simuladas",
    )

    parser.add_argument("--path", "-p", help="Caminho para a pasta contendo o dataset")
    args = parser.parse_args()
    if args.analyze and not args.path:
        print("É necessário informar o caminho para o dataset")
        exit(1)
    if args.analyze and args.simulate:
        print(
            "Não é possível gerar os dados e simular uma partida ao mesmo tempo. Faça a simulação primeiro e depois analise os resultados."
        )
        exit(1)
    return args


if __name__ == "__main__":
    args = checkArgs()
    main(
        args.simulate,
        args.analyze,
        args.path,
        not args.no_graphs,
        args.simulation_count,
    )
