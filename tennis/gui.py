from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markov Tennis Simulator")

        self._matchesWindow = MatchesWindow()
        self._matchesWindow.setParent(self)
        self._gamesWindow = GameWindow()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Markov Tennis Simulator"))
        showSimsButton = QPushButton("Show Simulations")
        showMatchesButton = QPushButton("Show Matches")
        showMatchesButton.clicked.connect(self.showMatchesWindow)
        exitButton = QPushButton("Sair")
        exitButton.clicked.connect(self.quit)
        layout.addWidget(showSimsButton)
        layout.addWidget(showMatchesButton)
        layout.addWidget(QPushButton("Analisar Games"))
        layout.addWidget(QPushButton("Analisar Sets"))
        layout.addWidget(exitButton)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def showMatchesWindow(self, checked):
        self._matchesWindow.show()

    def showGamesWindow(self, game):
        self._gamesWindow.show()

    def setTargetGame(self, game):
        self._gamesWindow.setGame(game)

    def quit(self, checked):
        exit(0)


test_items = {
    "3fb5hg": {
        "result": "P",
        "probP": 0.7,
        "probQ": 0.3,
        "date": "2020-01-01",
        "gamesP": 3,
        "gamesQ": 2,
    },
    "3ffa23": {
        "result": "Q",
        "probP": 0.9,
        "probQ": 0.1,
        "date": "2020-01-01",
        "gamesP": 3,
        "gamesQ": 2,
    },
}


class MatchesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matches")
        self.setFixedSize(QSize(400, 400))
        layout = QVBoxLayout()
        title = QLabel("Matches")
        title.setAlignment(Qt.AlignCenter)
        self._showGameDetailsButton = QPushButton("Show Game Details")
        self._showGameDetailsButton.setDisabled(True)
        self._matchSelectComboBox = QComboBox()
        self._matchSelectComboBox.addItem("Selecione um match...")
        for item in test_items.keys():
            self._matchSelectComboBox.addItem("{}".format(item))
            self._matchSelectComboBox.currentTextChanged.connect(self.setMatchByText)
        self._infoText = QLabel("Id da partida:\n\nResultado:\n\nProbP:\n\nProbQ:\n\n")

        layout.addWidget(title)
        layout.addWidget(self._matchSelectComboBox)
        layout.addWidget(self._infoText)
        layout.addWidget(self._showGameDetailsButton)

        self.setLayout(layout)

    def setParent(self, parent):
        self._parent = parent

    def setMatchByText(self, text):
        if text == "Selecione um match...":
            self._infoText.setText("Resultado: ")
            self._showGameDetailsButton.setDisabled(True)
            return
        itemData = test_items[text]
        self._infoText.setText(
            "Id da partida: {}\n\nResultado: {}\n\nProbP: {}\n\nProbQ: {}\n\n".format(
                text, itemData["result"], itemData["probP"], itemData["probQ"]
            )
        )
        self._showGameDetailsButton.setDisabled(False)
        self._showGameDetailsButton.clicked.connect(self._parent.showGamesWindow)
        self._parent.setTargetGame(text)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Games")
        self.setFixedSize(QSize(400, 400))
        self._game = None
        layout = QVBoxLayout()
        title = QLabel("Games")
        self._gameDataText = QLabel("Jogo: ")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(self._gameDataText)

        self.setLayout(layout)

    def setGame(self, game):
        self._game = game
        self._gameDataText.setText("Jogo: {}".format(game))
