import PyQt5.QtWidgets as Qt  # interface
from PyQt5 import QtCore, QtGui
import os  # os interaction
import glob  # file listing
import sys  # system functions
import json  # handle json data
from tkinter import filedialog  # file choosing ui


class IGameLauncher(Qt.QMainWindow):
    """Main UI for the game launcher app"""

    class GameTile(Qt.QWidget):
        """Object that represents a tile to display the game"""

        def __init__(self, gameName:str, gameSettings:list):
            """Builds a tile for a given game"""
            super().__init__()
            self.gameName = gameName
            self.gameSettings = gameSettings
            self.size = (240, 350)
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
            self.mainLayout.addWidget(self.playButton)


    def start(self):
        """Starts and launches the UI"""
        super().__init__()  # initialise the UI
        self.setWindowTitle("IGameLauncher")
        self.readData()  # get the session data
        self.buildUi()  # build the UI elements
        self.showMaximized()  # maximize the window
        self.show()  # display the UI
    
    def readData(self):
        """Reads the session data, or creates an empty file"""
        if not os.path.exists("data.json"):
            with open("data.json", "w", encoding="utf-8") as dataFile:
                #json.dump({}, dataFile, indent=4)
                test = {"Beat Saber":{"folder":"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber", "exe":"Beat Saber.exe"},
                        "Starfield":{"folder":"C:\\Users\\ilwan\\Documents\\Logiciels\\Starfield", "exe":"Starfield.exe"},
                        "No Man's Sky":{"folder":"C:\\Users\\ilwan\\Documents\\Logiciels\\No Man's Sky", "exe":"Binaries\\NMS.exe"}}
                json.dump(test, dataFile, indent=4)
        with open("data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
    
    def buildUi(self):
        """build the UI elements"""
        self.centralWidget = Qt.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = Qt.QGridLayout(self.centralWidget)
        self.nbColumns = 5  # number of columns for the tiles
        self.currentLine, self.currentColumn = 0, 0
        self.tiles = {}
        
        for game, settings in self.data.items():
            # creates and add the tiles
            self.currentColumn += 1
            if self.currentColumn >= self.nbColumns:  # check if we need to change line
                self.currentColumn = 0
                self.currentLine += 1
            tile = self.GameTile(game, settings)
            self.tiles[game] = tile
            self.mainLayout.addWidget(tile, self.currentLine, self.currentColumn, alignment=QtCore.Qt.AlignCenter)
            

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
