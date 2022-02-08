"""
Este arquivo define a classe "Markov", que representa um modelo de Markov genérico.
"""
import numpy as np
from typing import List, Type


class MarkovNode:
    """
    A classe que representa um determinado nó no grafo de Markov.
    """

    _nodes = {}
    _originalNodeData = {}

    def __init__(self, name, probP, probQ, nodeP: str, nodeQ: str):
        """
        Inicializa um novo nó do grafo de Markov.

        Args:
            name (str): O nome do nó.
            probP (float): A probabilidade de P vencer.
            probQ (float): A probabilidade de Q vencer.
            nodeP (MarkovNode): O nó associado à vitória de P.
            nodeQ (MarkovNode): O nó Q à vitória de Q.
            nodeList (List[MarkovNode]): A lista de nós.
        """
        self._name = name
        self._probP = probP
        self._probQ = probQ
        if nodeP != None:
            self._nodeP = MarkovNode.requestNode(nodeP)
        else:
            self._nodeP = None
        if nodeQ != None:
            self._nodeQ = MarkovNode.requestNode(nodeQ)
        else:
            self._nodeQ = None

    def __str__(self):
        return "({name}: ({NodeQ}, {NodeP}))".format(
            name=self._name, NodeP=self._nodeP, NodeQ=self._nodeQ
        )

    def requestNode(node: str):
        print("building node", node)
        if not node:
            return MarkovNode(None, None, None, None, None)
        if node in MarkovNode._nodes:
            print("node", node, "already exists")
            return MarkovNode._nodes[node]
        print("creating node with id", node)
        assert node != None
        nodeP: str = MarkovNode._originalNodeData[node]["nodeP"]
        nodeQ: str = MarkovNode._originalNodeData[node]["nodeQ"]
        MarkovNode._nodes[node] = MarkovNode(
            node,
            MarkovNode._originalNodeData[node]["probP"],
            MarkovNode._originalNodeData[node]["probQ"],
            MarkovNode.requestNode(nodeP)._name,
            MarkovNode.requestNode(nodeQ)._name,
        )
        return MarkovNode._nodes[node]

    def setNodeData(nodeData):
        MarkovNode._originalNodeData = nodeData
