"""
Este arquivo define a classe "Markov", que representa um modelo de Markov genérico.
"""
import numpy as np
from typing import List, Type
from random import seed, random

overridenProbabilityP = 0.5
overridenProbabilityQ = 0.5


class MarkovGraph:
    def __init__(self, initialNode, tgtSeed):
        self._initialNode = initialNode
        self._currentNode = initialNode
        self._seed = tgtSeed
        seed(tgtSeed)

    def getNextNode(self):
        print("Current node: ")
        print(self._currentNode)
        (nodeP, nodeQ) = self._currentNode.getNextNodes()
        print("NodeP: " + nodeP.__str__())
        print("NodeQ: " + nodeQ.__str__())
        if nodeP == None or nodeQ == None:
            return
        result = random()
        print("Random: " + str(result))
        if result < self._currentNode.getProbP():
            self._currentNode = nodeP
        else:
            self._currentNode = nodeQ
        print("Next node: " + self._currentNode.__str__())

    def getCurrentNode(self):
        return self._currentNode

    def simulateGame(self):
        (nodeP, nodeQ) = self._currentNode.getNextNodes()
        while nodeP != None and nodeQ != None:
            self.getNextNode()
            (nodeP, nodeQ) = self._currentNode.getNextNodes()
        print("Game ended. Last node was: ", self._currentNode.__str__())


class MarkovNode:
    """
    A classe que representa um determinado nó no grafo de Markov.
    """

    _nodes = {}

    def __init__(self, name, probP, probQ, nodeP: str, nodeQ: str):
        """
        Inicializa um novo nó do grafo de Markov.

        Args:
            name (str): O nome do nó.
            probP (float): A probabilidade de P vencer.
            probQ (float): A probabilidade de Q vencer.
            nodeP (MarkovNode): O nó associado à vitória de P.
            nodeQ (MarkovNode): O nó Q à vitória de Q.
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
        """
        if overridenProbabilityP != None:
            return overridenProbabilityP
        return self._probP

    def getProbQ(self):
        """
        Retorna a probabilidade de vitória de Q.
        """
        if overridenProbabilityQ != None:
            return overridenProbabilityQ
        return self._probQ

    def getName(self):
        """
        Retorna o nome (identificador) do nó.
        """
        return self._name

    def updateProbP(self, probP):
        """
        Atualiza a probabilidade de vitória de P.
        """
        self._probP = probP

    def updateProbQ(self, probQ):
        """
        Atualiza a probabilidade de vitória de Q.
        """
        self._probQ = probQ

    def populateNodes():
        """
        Popula os nós do grafo de Markov.
        """
        for key in MarkovNode._nodes:
            nodePName = MarkovNode._nodes[key]._nodeP
            nodeQName = MarkovNode._nodes[key]._nodeQ
            if nodePName != None:
                MarkovNode._nodes[key]._nodeP = MarkovNode._nodes[nodePName]
            if nodeQName != None:
                MarkovNode._nodes[key]._nodeQ = MarkovNode._nodes[nodeQName]

    def debug():
        for key in MarkovNode._nodes:
            print(MarkovNode._nodes[key])

    def getNodes():
        """
        Retorna os nós registrados no grafo de Markov.
        """
        return list(MarkovNode._nodes.values())

    def getNodeById(id: str):
        return MarkovNode._nodes[id]

    def getNextNodes(self):
        if self._nodeP == None or self._nodeQ == None:
            return (None, None)
        return (self._nodeP, self._nodeQ)
