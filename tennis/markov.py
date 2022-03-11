"""
Este arquivo define a classe "Markov", que representa um modelo de Markov genérico.
"""
import numpy as np
from random import seed, random
import json
from time import strftime
import os

from pprint import pprint

overridenProbabilityP = 0.55
overridenProbabilityQ = 1 - overridenProbabilityP


class MarkovGraph:
    """
    Classe que representa um conjunto de nós de um modelo de Markov voltado para a
    simulação de um game (conjunto de pontos) de tênis.
    O uso geral da classe segue o seguinte fluxo:
        - Criação dos nós da classe `MarkovNode`;
        - Instanciação da classe `MarkovGraph` usando o `MarkovNode` inicial como parâmetro
        e um valor aleatório como tgtSeed (sugestão: tempo atual em milissegundos);
        - Chamada de `simulateGame` para simular um game;
        - Chamada de `getResults` para obter os resultados em JSON, ou passar `True` para
        `simulateGame` no passo anterior para salvar os resultados em JSON de forma automática;
        - Chamada de `reset` para reiniciar o modelo para um novo game.
    """

    def __init__(self, initialNode, tgtSeed):
        """
        Construtor da classe.
        Args:
            initialNode (`MarkovNode`): Nó inicial do modelo.
            tgtSeed (int): Seed para o gerador de números aleatórios.
        """
        self._initialNode = initialNode
        self._currentNode = initialNode
        self._seed = tgtSeed
        self._pScore = 0
        self._qScore = 0
        self._logFileData = []
        seed(tgtSeed)

    def getNextNode(self):
        """
        Gera um novo valor aleatoriamente e atualiza a variável de instância "currentNode"
        com o próximo nó. Não faz nada se um dos próximos nós não existir. Também registra
        a operação no log da instância.
        """
        currentLogData = {}
        (nodeP, nodeQ) = self._currentNode.getNextNodes()
        currentLogData["originalNode"] = self._currentNode.toJson()
        if nodeP == None or nodeQ == None:
            return
        result = random()
        scorer = ""
        if result < self._currentNode.getProbP():
            self._currentNode = nodeP
            self._pScore += 1
            scorer = "p"
        else:
            self._currentNode = nodeQ
            self._qScore += 1
            scorer = "q"
        currentLogData["resultValue"] = result
        currentLogData["partialResults"] = "{}-{}".format(self._pScore, self._qScore)
        currentLogData["scorer"] = scorer
        self._logFileData.append(currentLogData)

    def getCurrentNode(self):
        """
        Retorna o nó atual.

        Returns:
            `MarkovNode`: Nó atual.
        """
        return self._currentNode

    def simulateGame(self, shouldDumpResultsToFile=False):
        """
        Simula um game do jogo de tênis.
        Args:
            shouldDumpResultsToFile (bool): Se True, salva os resultados do game no arquivo de log.
                Os detalhes sobre o log estão descritos em `MarkovGraph.dumpResultsToFile`.
        """
        (nodeP, nodeQ) = self._currentNode.getNextNodes()
        while nodeP != None and nodeQ != None:
            self.getNextNode()
            (nodeP, nodeQ) = self._currentNode.getNextNodes()
        if shouldDumpResultsToFile:
            self.dumpResultsToFile()

    def getWinner(self):
        """
        Retorna o vencedor do game.

        Returns:
            str: "p" se o jogador P venceu o game, "q" se o jogador Q venceu o game.
        """
        return "p" if self._pScore > self._qScore else "q"

    def getResults(self):
        """
        Retorna os resultados do game formatados em JSON.

        Formato:


        O objeto retornado por este método possui a seguinte estrutura interna:

            {
                data: dados dos pontos do game
                gameResult: resultado do game
                winner: vencedor do game
            }
        O formato do objeto `gameResult` é o seguinte:

            {
                p: pontos do jogador P
                q: pontos do jogador Q
            }

        O formato de `winner` é uma string que pode ser "p" ou "q", indicando o vencedor do game.

        O objeto ``data`` tem a estrutura:

            {
                originalNode: o nó original a partir do qual o ponto foi processado;
                resultValue: valor aleatório (float) gerado pelo gerador de números aleatórios;
                partialResults: pontuação parcial até o momento, no formato X-Y, onde X
                é a pontuação do jogador P e Y é a pontuação do jogador Q;
            }

        O formato do objeto "originalNode" é descrito no método `MarkovNode.toJson`.
        """
        return {
            "gameData": self._logFileData,
            "gameResult": {"p": self._pScore, "q": self._qScore},
            "gameWinner": "p" if self._pScore > self._qScore else "q",
        }

    def dumpResultsToFile(self):
        """
        Salva os resultados do set no arquivo de log.

        O arquivo de log é armazenado em `/results/games/data-hora-do-jogo.json`

        A função é encarregada de criar o caminho, caso ele não exista.
        """
        currentTime = strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists(os.path.join("results", "games")):
            os.mkdir(os.path.join("results", "games"))

        with open(
            os.path.join("results", "games", "{}.json".format(currentTime)), "w"
        ) as logFile:
            logFile.write(self.getResults())

    def reset(self, tgtSeed):
        """
        Reseta o modelo para um novo game.
        Args:
            tgtSeed (int): Seed para o gerador de números aleatórios. Esse seed deve ser diferente
                do usado originalmente, para evitar que o gerador de números aleatórios gere
                os mesmos resultados.
        """
        self._currentNode = self._initialNode
        self._pScore = 0
        self._qScore = 0
        self._logFileData = []
        seed(tgtSeed)

    def getSeed(self):
        """
        Retorna o seed usado para gerar os números aleatórios.

        Returns:
            int: Seed usado para gerar os números aleatórios.
        """
        return self._seed


class MarkovNode:
    """
    A classe que representa um determinado nó no grafo de Markov.
    """

    _nodes = {}

    def __init__(self, name, probP, probQ, nodeP: str, nodeQ: str):
        """
        Inicializa um novo nó do grafo de Markov. Note que os nós `nodeP` e `nodeQ` devem
        existir à priori.

        Args:
            name (str): O nome do nó.
            probP (float): A probabilidade de P vencer.
            probQ (float): A probabilidade de Q vencer.
            nodeP (`MarkovNode`): O nó associado à vitória de P.
            nodeQ (`MarkovNode`): O nó associado à vitória de Q.
        """
        self._name = name

        self._probP = probP
        self._probQ = probQ

        self._nodeP = nodeP
        self._nodeQ = nodeQ

        MarkovNode._nodes[name] = self

    def __str__(self):
        nodeP = None
        nodeQ = None
        if self._nodeP != None:
            nodeP = self._nodeP._name
        if self._nodeQ != None:
            nodeQ = self._nodeQ._name
        return "({name}: ({NodeQ}, {NodeP}))".format(
            name=self._name, NodeP=nodeP, NodeQ=nodeQ
        )

    def getProbP(self):
        """
        Retorna a probabilidade de vitória de P.

        Returns:
            float: Probabilidade de vitória de P.
        """
        if overridenProbabilityP != None:
            return overridenProbabilityP
        return self._probP

    def getProbQ(self):
        """
        Retorna a probabilidade de vitória de Q.

        Returns:
            float: Probabilidade de vitória de Q.
        """
        if overridenProbabilityQ != None:
            return overridenProbabilityQ
        return self._probQ

    def getName(self):
        """
        Retorna o nome (identificador) do nó.

        Returns:
            str: O nome do nó.
        """
        return self._name

    def updateProbP(self, probP):
        """
        Atualiza a probabilidade de vitória de P no nó atual.
        """
        self._probP = probP

    def updateProbQ(self, probQ):
        """
        Atualiza a probabilidade de vitória de Q no nó atual.
        """
        self._probQ = probQ

    def populateNodes():
        """
        Popula os nós do grafo de Markov.
        Por usar recursão durante a criação dos nós, o processo de instanciação
        é realizado em duas etapas: primeiramente, os nós são criados sem seus campos
        `nodeP` e `nodeQ` preenchidos. Depois, com todos os nós criados, os campos são
        populados.
        """
        for key in MarkovNode._nodes:
            nodePName = MarkovNode._nodes[key]._nodeP
            nodeQName = MarkovNode._nodes[key]._nodeQ
            if nodePName != None:
                MarkovNode._nodes[key]._nodeP = MarkovNode._nodes[nodePName]
            if nodeQName != None:
                MarkovNode._nodes[key]._nodeQ = MarkovNode._nodes[nodeQName]

    def getNodes():
        """
        Retorna os nós registrados no grafo de Markov.

        Returns:
            [`MarkovNode`]: Uma lista contendo os nós registrados no grafo de Markov.
        """
        return list(MarkovNode._nodes.values())

    def getNodeById(id: str):
        """
        Retorna um nó do grafo de Markov baseado em seu identificador.

        Returns:
            `MarkovNode`: O nó do grafo de Markov.
        """
        return MarkovNode._nodes[id]

    def getNextNodes(self):
        """
        Retorna uma tupla com os nós que podem ser visitados a partir do nó atual.

        Returns:
            (`MarkovNode`, `MarkovNode`): Uma tupla contendo os nós que podem ser visitados.
            A ordem é sempre a mesma, sendo que o primeiro elemento é o nó de vitória de P e
            o segundo elemento é o nó de vitória de Q.
        """
        if self._nodeP == None or self._nodeQ == None:
            return (None, None)
        return (self._nodeP, self._nodeQ)

    def toJson(self):
        """
        Converte as informações do nó para o formato JSON.

        A formatação dos dados é a seguinte:

            {
                "selfNode": identificador do nó atual,
                "nodeP": identificador do nó de vitória de P,
                "nodeQ": identificador do nó de vitória de Q,
            }

        Todos os valores são armazenados como strings.
        """
        return {
            "selfNode": self._name,
            "nodeP": self._nodeP._name if self._nodeP != None else None,
            "nodeQ": self._nodeQ._name if self._nodeQ != None else None,
        }
