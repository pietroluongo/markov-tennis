from time import time


def getSeedFromTime(iter: int):
    """
    Função auxiliar usada para obter um seed para o gerador de números aleatórios a partir
    do tempo atual.

    Returns:
        (int) tempo atual em milissegundos
    """
    return round(time() * 1000 * iter)


def mean(list):
    """
    Calcula a média de um vetor de números.

    Args:
        list (list): vetor de números

    Returns:
        (float) média dos números

    """
    return sum(list) / len(list)


def dp(list):
    """
    Calcula o desvio padrão de um vetor de números.

    Args:
        list (list): vetor de números

    Returns:
        (float) desvio padrão dos números

    """
    return (sum(list) / len(list)) ** 0.5
    iMean = mean(list)
    return (sum([(x - iMean) ** 2 for x in list]) / len(list)) ** 0.5
