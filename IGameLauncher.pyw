import PyQt5.QtWidgets as Qt  # interface
from PyQt5 import QtCore, QtGui
import functools  # tool to represent functions with arguments
import os  # os interaction
import glob  # file listing
import sys  # system functions
import json  # handle json data
from tkinter import filedialog  # file choosing ui


class IGameLauncher(Qt.QMainWindow):
    """Main UI for the game launcher app"""

    class AddPopup(Qt.QWidget):
        """A popup window"""

        def __init__(self):
            super().__init__()
            self.gameName = "Unnamed"
            self.data = {"folder": None, "exe": None}
            self.setWindowTitle("Add game")
            self.build()  # build the widgets
            self.setup()
            self.show()
        
        def build(self):
            """Build the widgets"""
            self.setFont(QtGui.QFont("Arial", 16))
            self.mainLayout = Qt.QVBoxLayout()
            self.setLayout(self.mainLayout)

            self.nameInput = Qt.QLineEdit()
            self.nameInput.setPlaceholderText("Enter game name")
            self.mainLayout.addWidget(self.nameInput)

            self.folderButton = Qt.QPushButton(text="Select game folder")
            self.mainLayout.addWidget(self.folderButton)

            self.exeButton = Qt.QPushButton(text="Select game executable")
            self.mainLayout.addWidget(self.exeButton)

            self.validationWidget = Qt.QWidget()
            self.validationLayout = Qt.QHBoxLayout()
            self.validationWidget.setLayout(self.validationLayout)
            self.mainLayout.addWidget(self.validationWidget)

            self.doneButton = Qt.QPushButton(text="Done")
            self.validationLayout.addWidget(self.doneButton)

            self.cancelButton = Qt.QPushButton(text="Cancel")
            self.validationLayout.addWidget(self.cancelButton)
        
        def setup(self):
            """Setup every widget"""
            self.folderButton.clicked.connect(self.selectFolder)
            self.exeButton.clicked.connect(self.selectExe)
        
        def selectFolder(self):
            """Select the game folder"""
            folderPath = filedialog.askdirectory(title="Select game folder")
            if folderPath:
                self.data["folder"] = folderPath

        def selectExe(self):
            """Select the game executable"""
            exePath = filedialog.askopenfile(filetypes=(("application", "*.exe"),("all", "*.*")), initialdir=self.data["folder"], title="Select game executable")
            if exePath:
                self.exePath = exePath
    

    class GameTile(Qt.QWidget):
        """Object that represents a tile to display the game"""
        size = (240, 350)

        def __init__(self, gameName:str, gameSettings:dict):
            """Builds a tile for a given game"""
            super().__init__()
            self.gameName = gameName
            self.gameSettings = gameSettings
            self.build()
        
        def build(self):
            """Builds the tile widget"""
            self.mainLayout = Qt.QVBoxLayout()
            self.setLayout(self.mainLayout)

            self.nameLabel = Qt.QLabel(text=self.gameName)
            self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.nameLabel.setFont(QtGui.QFont("Arial", 20))
            self.nameLabel.setWordWrap(True)
            self.mainLayout.addWidget(self.nameLabel)

            self.bannerButton = Qt.QPushButton()
            self.bannerButton.setFixedSize(self.size[0], self.size[1])
            if os.path.exists(f"banners\\{self.gameName}.png"):
                self.icon = QtGui.QIcon(f"banners\\{self.gameName}.png")
                self.bannerButton.setIcon(self.icon)
                self.bannerButton.setIconSize(QtCore.QSize(self.size[0], self.size[1]))
            self.mainLayout.addWidget(self.bannerButton)

            self.playButton = Qt.QPushButton(text="PLAY")
            self.playButton.setFont(QtGui.QFont("Arial", 24))
            self.playButton.setFixedHeight(60)
            self.mainLayout.addWidget(self.playButton)


    def start(self):
        """Starts and launches the UI"""
        super().__init__()  # initialise the UI
        self.setWindowTitle("IGameLauncher")
        self.readData()  # get the session data
        self.reload(firstLoad=True)  # load the UI
        self.showMaximized()  # maximize the window
        self.show()  # display the UI
    
    def readData(self):
        """Reads the session data, or creates an empty file"""
        if not os.path.exists("data.json"):
            with open("data.json", "w", encoding="utf-8") as dataFile:
                #json.dump({}, dataFile, indent=4)
                test = {"Starfield":{"folder":"C:\\Users\\ilwan\\Documents\\Logiciels\\Starfield", "exe":"Starfield.exe"},
                        "No Man's Sky":{"folder":"C:\\Users\\ilwan\\Documents\\Logiciels\\No Man's Sky", "exe":"Binaries\\NMS.exe"},
                        "FNAF Security Breach":{"folder":"D:\\Ilwan\\Logiciels\\FNAF Security Breach", "exe":"fnaf9.exe"},
                        "Geometry Dash":{"folder":"D:\\Ilwan\\Logiciels\\Geometry Dash", "exe":"GeometryDash.exe"},
                        "House Flipper":{"folder":"D:\\Ilwan\\Logiciels\\House Flipper", "exe":"HouseFlipper.exe"},
                        "PC Building Simulator 2":{"folder":"D:\\Ilwan\\Logiciels\\PC Building Simulator 2", "exe":"PCBS2.exe"},
                        "Subnautica Below Zero":{"folder":"D:\\Ilwan\\Logiciels\\Subnautica Below Zero", "exe":"SubnauticaZero.exe"}}
                json.dump(test, dataFile, indent=4)
        with open("data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
    
    def reload(self, firstLoad=False):
        """reloads the whole interface with current settigns"""
        if not firstLoad:
            self.clear(self.scrollLayout)
        self.buildUi()
        self.setup()
    
    def clear(self, layout):
        """clear the whole layout"""
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)  # delete widget
    
    def buildUi(self):
        """build the UI elements"""
        self.nbColumns = 5  # number of columns for the tiles
        self.currentLine, self.currentColumn = 0, 0
        self.tiles = {}

        self.centralWidget = Qt.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = Qt.QVBoxLayout(self.centralWidget)

        self.scrollZone = Qt.QScrollArea()
        self.scrollZone.setWidgetResizable(True)
        self.scrollZone.setStyleSheet("QScrollArea { border: none; }")
        self.scrollInnerWidget = Qt.QWidget()
        self.scrollLayout = Qt.QGridLayout()
        self.scrollZone.setWidget(self.scrollInnerWidget)
        self.scrollInnerWidget.setLayout(self.scrollLayout)
        self.mainLayout.addWidget(self.scrollZone)
        
        for game, settings in self.data.items():
            # creates and add the tiles
            tile = self.GameTile(game, settings)
            self.tiles[game] = tile
            self.scrollLayout.addWidget(tile, self.currentLine, self.currentColumn, alignment=QtCore.Qt.AlignCenter)

            self.currentColumn += 1
            if self.currentColumn >= self.nbColumns:  # check if we need to change line
                self.currentColumn = 0
                self.currentLine += 1
        self.addButton = Qt.QPushButton()
        self.addButton.setFixedSize(150, 150)
        self.addButton.setIcon(QtGui.QIcon("assets\\add.png"))
        self.addButton.setIconSize(QtCore.QSize(130, 130))
        self.scrollLayout.addWidget(self.addButton, self.currentLine, self.currentColumn, alignment=QtCore.Qt.AlignCenter)
    
    def setup(self):
        """Setup all the functions to interract with the UI"""
        for game, tile in self.tiles.items():
            tile.playButton.clicked.connect(functools.partial(self.launchGame, f"{tile.gameSettings['folder']}\\{tile.gameSettings['exe']}"))
        self.addButton.clicked.connect(self.askGame)
    
    def launchGame(self, exePath:str):
        """Launches the given exe file"""
        if exePath:
            currentDir = os.getcwd()
            os.chdir("\\".join(exePath.split("\\")[:-1]))
            os.startfile(exePath)
            os.chdir(currentDir)
    
    def askGame(self):
        """Asks to add a new game"""
        self.askPopup = self.AddPopup()
        self.askPopup.doneButton.clicked.connect(lambda: self.addGame(self.askPopup.gameName, self.askPopup.data))

    def addGame(self, name, data):
        """Adds a new game to the library"""
        pass


if __name__ == "__main__":  # if the file is executed directly
    # scale dpi
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        Qt.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        Qt.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    # launch app
    App = Qt.QApplication(sys.argv)  # creating the app
    Window = IGameLauncher()  # creating the GUI
    Window.start()  # starting the GUI
    App.exec_()  # executing the app
