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


class MarkovData:
    """
    Classe que modela um conjunto de dados para uma cadeia de markov.
    """

    def __init__(self, transitions: List[float], states: List[str]):
        """
        Construtor da classe.
        Args:
            transitions (List[float]): a matriz 2D de transições de estados. A matriz é da forma:

                `[
                    [0.1, 0.2, 0.3, 0.4],
                    [0.5, 0.6, 0.7, 0.8],
                    [0.9, 1.0, 1.1, 1.2],
                    [1.3, 1.4, 1.5, 1.6]
                ]`
                Onde cada elemento [i, j] representa a chance de mudança do estado i para o estado j.
            states (List[str]): uma lista com os possíveis estados. A ordem dos estados deve seguir a ordem da matriz de transições - ou seja, o i-ésimo estado é associado à i-ésima coluna/linha.
        """
        self._transitions: List[float] = np.atleast_2d(transitions)
        self._states: List[str] = states
        self.__all__ = 1

    @property
    def transitions(self):
        """
        Retorna a matriz de transições.
        Retorna:
            List[float]: a matriz 2D de transições de estados.
        """
        return self._transitions

    @property
    def states(self):
        """
        Retorna o próximo estado da cadeia de markov a partir do estado atual.
        Returns:
            (str) o próximo estado.
        """
        return self._states


class MarkovChain:
    """
    A classe que modela uma cadeia de markov a partir de informações encapsuladas em um `MarkovData`.
    """

    def __init__(self, data):
        """
        Inicializa uma cadeia de markov a partir de um conjunto de dados expressos como `MarkovData`.

        Args:
            data (MarkovData): um objeto que encapsula as informações da cadeia.
        """
        self.transitions: List[float] = data.transitions()
        self.possibleStates: List[str] = data.states()

    def nextState(self, currentState):
        """
        Retorna o próximo estado da cadeia de markov a partir do estado atual.
        Args:
            currentState (str): o estado atual.

        Retorna:
            (str) o próximo estado.
        """
        return []
