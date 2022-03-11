from markov import MarkovGraph
from time import time, strftime
from typing import Type
from utils import getSeedFromTime
import os
import json


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

    def toJSON(self):
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
                        },
                        winner (str): "p" se o vencedor for P, e "q" se o vencedor for Q
                    },
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
        A formatação do arquivo é descrita em `toJSON`.
        """
        currentTime = strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists("results"):
            os.mkdir("results")
        if not os.path.exists(os.path.join("results", "sets")):
            os.mkdir(os.path.join("results", "sets"))

        with open(
            os.path.join("results", "sets", "{}.json".format(currentTime)), "w"
        ) as outputFile:
            outputFile.write(self.toJSON().__str__())

    def reset(self):
        """
        Reseta o jogo.
        """
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

    _idx = 0
    """
    Variável estática de classe usada para gerar um ID único para cada partida.
    """

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
            self._sets.append(self._set.toJSON())
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
            A estrutura de `data` é descrita em detalhes em `TennisSet.toJSON`.
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
                "results", "matches", "{}-{}.json".format(currentTime, TennisMatch._idx)
            ),
            "w",
        ) as outputFile:
            outputFile.write(json.dumps(self.toJSON()))
            TennisMatch._idx += 1

    def getWinner(self):
        """
        Retorna o vencedor do game atual.

        Returns:
            (str): "p", se o vencedor for P, e "q", se o vencedor for Q
        """
        return self._winner
