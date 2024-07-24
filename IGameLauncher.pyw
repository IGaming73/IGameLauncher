import PyQt5.QtWidgets as Qt  # interface
from PyQt5 import QtCore, QtGui
from PIL import Image  # image processing
import functools  # tool to represent functions with arguments
import os  # os interaction
import glob  # file listing
import time  # delay and time
import sys  # system functions
import json  # handle json data
from tkinter import filedialog  # file choosing ui


class IGameLauncher(Qt.QMainWindow):
    """Main UI for the game launcher app"""

    class AddPopup(Qt.QWidget):
        """A popup window to add a game"""

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

            self.folderWidget = Qt.QWidget()
            self.folderLayout = Qt.QHBoxLayout()
            self.folderWidget.setLayout(self.folderLayout)
            self.mainLayout.addWidget(self.folderWidget)

            self.folderButton = Qt.QPushButton(text="Select game folder")
            self.folderLayout.addWidget(self.folderButton)
            
            self.folderLabel = Qt.QLabel()
            self.folderLayout.addWidget(self.folderLabel)

            self.exeWidget = Qt.QWidget()
            self.exeLayout = Qt.QHBoxLayout()
            self.exeWidget.setLayout(self.exeLayout)
            self.mainLayout.addWidget(self.exeWidget)

            self.exeButton = Qt.QPushButton(text="Select game executable")
            self.exeLayout.addWidget(self.exeButton)

            self.exeLabel = Qt.QLabel()
            self.exeLayout.addWidget(self.exeLabel)

            self.bannerWidget = Qt.QWidget()
            self.bannerLayout = Qt.QHBoxLayout()
            self.bannerWidget.setLayout(self.bannerLayout)
            self.mainLayout.addWidget(self.bannerWidget)

            self.bannerButton = Qt.QPushButton(text="Select game banner")
            self.bannerLayout.addWidget(self.bannerButton)

            self.bannerLabel = Qt.QLabel()
            self.bannerLayout.addWidget(self.bannerLabel)

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
            self.nameInput.editingFinished.connect(self.updateName)
            self.folderButton.clicked.connect(self.selectFolder)
            self.exeButton.clicked.connect(self.selectExe)
            self.bannerButton.clicked.connect(self.askBanner)
            self.cancelButton.clicked.connect(self.close)
            self.doneButton.clicked.connect(self.done)
        
        def selectFolder(self):
            """Select the game folder"""
            folderPath = filedialog.askdirectory(title="Select game folder")
            if folderPath:
                self.data["folder"] = folderPath.replace("/", "\\")
                folderName = folderPath.replace("/", "\\").split("\\")[-1]
                self.folderLabel.setText(folderName)
                if self.gameName == "Unnamed":
                    self.nameInput.setText(folderName)
                    self.updateName()

        def selectExe(self):
            """Select the game executable"""
            exeFile = filedialog.askopenfile(filetypes=(("application", "*.exe"),("all", "*.*")), initialdir=self.data["folder"], title="Select game executable")
            if exeFile:
                exePath = exeFile.name
                exeFile.close()
                self.data["exe"] = exePath.replace("/", "\\")
                self.exeLabel.setText(exePath.replace("/", "\\").split("\\")[-1])
        
        def updateName(self):
            """Updates the game name"""
            newGameName = self.nameInput.text()
            self.gameName = newGameName
        
        def askBanner(self):
            """Asks for an image file as a banner"""
            bannerFile = filedialog.askopenfile(filetypes=(("image", "*.png *.jpg *.jpeg *.webp"),("all", "*.*")), initialdir=self.data["folder"], title="Select game executable")
            if bannerFile:
                self.bannerPath = bannerFile.name
                bannerFile.close()
                self.bannerLabel.setText(self.bannerPath.replace("/", "\\").split("\\")[-1])
                # cropping the banner image
                bannerImage = Image.open(self.bannerPath)
                width, height = bannerImage.size
                currentRatio = width / height
                ratio = IGameLauncher.GameTile.ratio
                if currentRatio > ratio:
                    newWidth = round(height * ratio)
                    left = (width - newWidth) // 2
                    right = left + newWidth
                    bannerImage = bannerImage.crop((left, 0, right, height))
                elif currentRatio < ratio:
                    newHeight = round(width / ratio)
                    top = (height - newHeight) // 2
                    bottom = top + newHeight
                    bannerImage = bannerImage.crop((0, top, width, bottom))
                bannerImage.save(f"banners\\banner.png")
        
        def done(self):
            """When the done button is clicked"""
            if os.path.exists(f"banners\\banner.png"):
                os.rename(f"banners\\banner.png", f"banners\\{self.gameName}.png")
            self.close()
    

    class GameTile(Qt.QWidget):
        """Object that represents a tile to display the game"""
        size = (240, 350)
        ratio = size[0]/size[1]

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
            self.nameLabel.setFixedHeight(100)
            self.nameLabel.setWordWrap(True)
            self.mainLayout.addWidget(self.nameLabel)

            self.bannerButton = Qt.QPushButton()
            self.bannerButton.setFixedSize(self.size[0], self.size[1])
            if os.path.exists(f"banners\\{self.gameName}.png"):
                self.icon = QtGui.QIcon(f"banners\\{self.gameName}.png")
            else:
                self.icon = QtGui.QIcon("assets\\banner.png")
            self.bannerButton.setIcon(self.icon)
            self.bannerButton.setIconSize(QtCore.QSize(self.size[0]-6, self.size[1]-6))
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
                json.dump({}, dataFile, indent=4)
        with open("data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
    
    def writeData(self):
        """Completely overwrite the data in the json file"""
        with open("data.json", "w", encoding="utf-8") as dataFile:
            json.dump(self.data, dataFile, indent=4)
    
    def reload(self, firstLoad:bool=False):
        """reloads the whole interface with current settigns"""
        if not firstLoad:
            self.clear(self.scrollLayout)
        self.buildUi()
        self.setup()
    
    def clear(self, layout:Qt.QLayout):
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
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
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
            tile.playButton.clicked.connect(functools.partial(self.launchGame, tile.gameSettings["exe"]))
            tile.bannerButton.clicked.connect(functools.partial(self.modifyGame, tile.gameName))
        self.addButton.clicked.connect(self.askGame)
    
    def launchGame(self, exePath:str):
        """Launches the given exe file"""
        if exePath:
            currentDir = os.getcwd()
            folderToMove = "\\".join(exePath.replace("/", "\\").split("\\")[:-1])
            os.chdir(folderToMove)
            os.startfile(exePath)
            os.chdir(currentDir)
    
    def modifyGame(self, gameName:str):
        """Modify the settings of a game or remove it, creates the interface"""
        self.clear(self.scrollLayout)
        
        self.infosWidget = Qt.QWidget()
        self.infosLayout = Qt.QVBoxLayout()
        self.infosLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.infosWidget.setLayout(self.infosLayout)
        self.scrollLayout.addWidget(self.infosWidget)

        self.modifyWidget = Qt.QWidget()
        self.modifyLayout = Qt.QVBoxLayout()
        self.modifyLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.modifyWidget.setLayout(self.modifyLayout)
        self.scrollLayout.addWidget(self.modifyWidget)

        self.buildInfosLayout(gameName)
    
    def buildInfosLayout(self, gameName:str):
        """Builds the content of the infos layout in the settings editor"""
        bannerX, bannerY = round(self.GameTile.size[0]*1.5), round(self.GameTile.size[1]*1.5)
        self.bannerImage = Qt.QLabel()
        self.bannerImage.setFixedSize(bannerX, bannerY)
        if os.path.exists(f"banners\\{gameName}.png"):
            self.bannerImage.setPixmap(QtGui.QPixmap(f"banners\\{gameName}.png").scaled(bannerX, bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.bannerImage.setPixmap(QtGui.QPixmap("assets\\banner.png").scaled(bannerX, bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.infosLayout.addWidget(self.bannerImage)

        self.nameLabel = Qt.QLabel(text=gameName)
        self.nameLabel.setFont(QtGui.QFont("Arial", 26))
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setWordWrap(True)
        self.infosLayout.addWidget(self.nameLabel)

        self.pathLabel = Qt.QLabel(text=self.data[gameName]["exe"].replace("\\", "\\ "))
        self.pathLabel.setFont(QtGui.QFont("Arial", 14))
        self.pathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pathLabel.setWordWrap(True)
        self.infosLayout.addWidget(self.pathLabel)

        self.playButton = Qt.QPushButton(text="PLAY")
        self.playButton.setFont(QtGui.QFont("Arial", 24))
        self.playButton.setFixedHeight(60)
        self.infosLayout.addWidget(self.playButton)
        self.playButton.clicked.connect(lambda: self.launchGame(self.data[gameName]["exe"]))
    
    def askGame(self):
        """Asks to add a new game"""
        self.askPopup = self.AddPopup()
        self.askPopup.doneButton.clicked.connect(lambda: self.addGame(self.askPopup.gameName, self.askPopup.data))

    def addGame(self, name:str, data:dict):
        """Adds a new game to the library"""
        self.data[name] = data
        self.writeData()
        self.reload()


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
