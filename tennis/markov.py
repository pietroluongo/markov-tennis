"""
Este arquivo define a classe "Markov", que representa um modelo de Markov genérico.
"""
import numpy as np
from typing import List, Type


class MarkovNode:
    """
    A classe que representa um determinado nó no grafo de Markov.
    """

    def __init__(self, name, probP, probQ, nodeP: str, nodeQ: str, nodeList):
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
        assert nodeP != None
        assert nodeQ != None
        if nodeP != None:
            self._nodeP = nodeList[nodeP]
        if nodeQ != None:
            self._nodeQ = nodeList[nodeQ]

    def __str__(self):
        return "({name}: ({NodeQ}, {NodeP}))".format(
            name=self._name, NodeP=self._nodeP, NodeQ=self._nodeQ
        )