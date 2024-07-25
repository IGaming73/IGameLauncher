import PIL.JpegImagePlugin
import PyQt5.QtWidgets as Qt  # interface
from PyQt5 import QtCore, QtGui
from PIL import Image  # image processing
from PIL.JpegImagePlugin import JpegImageFile as ImageFile  # image object
import functools  # tool to represent functions with arguments
import os  # os interaction
import glob  # file listing
import time  # delay and time
import sys  # system functions
import pyshortcuts  # create app shortcuts
import darkdetect  # detect dark mode
import json  # handle json data
from tkinter import filedialog  # file choosing ui


class IGameLauncher(Qt.QMainWindow):
    """Main UI for the game launcher app"""

    class AddWidget(Qt.QWidget):
        """A widget to add a game"""
        defaultName = "Game name"

        def __init__(self):
            super().__init__()
            self.gameName = self.defaultName
            self.data = {"folder": None, "exe": None}
            self.build()  # build the widgets
            self.setup()
        
        def build(self):
            """Build the widgets"""
            self.mainLayout = Qt.QHBoxLayout()
            self.setLayout(self.mainLayout)
            self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)

            self.leftWidget = Qt.QWidget()
            self.leftLayout = Qt.QVBoxLayout()
            self.leftLayout.setAlignment(QtCore.Qt.AlignCenter)
            self.leftWidget.setLayout(self.leftLayout)
            self.mainLayout.addWidget(self.leftWidget)

            self.rightWidget = Qt.QWidget()
            self.rightLayout = Qt.QVBoxLayout()
            self.rightLayout.setAlignment(QtCore.Qt.AlignCenter)
            self.rightWidget.setLayout(self.rightLayout)
            self.mainLayout.addWidget(self.rightWidget)
            
            self.buildLeft()
        
        def buildLeft(self):
            """Build the widgets on the left side"""
            self.bannerX, self.bannerY = IGameLauncher.GameTile.bigSize[0], IGameLauncher.GameTile.bigSize[1]
            self.bannerImage = Qt.QLabel()
            self.bannerImage.setFixedSize(self.bannerX, self.bannerY)
            if darkdetect.isDark():
                self.bannerImage.setPixmap(QtGui.QPixmap("assets\\dark\\banner.png").scaled(self.bannerX, self.bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.bannerImage.setPixmap(QtGui.QPixmap("assets\\light\\banner.png").scaled(self.bannerX, self.bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.leftLayout.addWidget(self.bannerImage)

            self.nameLabel = Qt.QLabel(text=self.defaultName)
            self.nameLabel.setFont(QtGui.QFont("Arial", 32))
            self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.nameLabel.setWordWrap(True)
            self.leftLayout.addWidget(self.nameLabel)

            self.pathLabel = Qt.QLabel()
            self.pathLabel.setFont(QtGui.QFont("Arial", 16))
            self.pathLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.pathLabel.setWordWrap(True)
            self.leftLayout.addWidget(self.pathLabel)

            self.buildRight()
        
        def buildRight(self):
            """Build the widgets on the right side"""
            self.nameWidget = Qt.QWidget()
            self.nameLayout = Qt.QHBoxLayout()
            self.nameWidget.setLayout(self.nameLayout)
            self.rightLayout.addWidget(self.nameWidget)

            self.nameInput = Qt.QLineEdit()
            self.nameInput.setPlaceholderText("Enter game name")
            self.nameInput.setText(self.defaultName)
            self.nameInput.setFixedHeight(50)
            self.nameInput.setFont(QtGui.QFont("Arial", 20))
            self.nameLayout.addWidget(self.nameInput)
            self.nameLayout.addStretch()

            self.folderWidget = Qt.QWidget()
            self.folderLayout = Qt.QHBoxLayout()
            self.folderWidget.setLayout(self.folderLayout)
            self.rightLayout.addWidget(self.folderWidget)

            self.folderInput = Qt.QLineEdit()
            self.folderInput.setPlaceholderText("Game folder path")
            self.folderInput.setFixedHeight(50)
            self.folderInput.setFont(QtGui.QFont("Arial", 20))
            self.folderLayout.addWidget(self.folderInput)

            self.folderButton = Qt.QPushButton()
            self.folderButton.setFixedSize(50, 50)
            if darkdetect.isDark():
                self.folderButton.setIcon(QtGui.QIcon("assets\\dark\\folder.png"))
            else:
                self.folderButton.setIcon(QtGui.QIcon("assets\\light\\folder.png"))
            self.folderButton.setIconSize(QtCore.QSize(35, 35))
            self.folderLayout.addWidget(self.folderButton)
            self.folderLayout.addStretch()

            self.exeWidget = Qt.QWidget()
            self.exeLayout = Qt.QHBoxLayout()
            self.exeWidget.setLayout(self.exeLayout)
            self.rightLayout.addWidget(self.exeWidget)

            self.exeInput = Qt.QLineEdit()
            self.exeInput.setPlaceholderText("Game executable path")
            self.exeInput.setFixedHeight(50)
            self.exeInput.setFont(QtGui.QFont("Arial", 20))
            self.exeLayout.addWidget(self.exeInput)

            self.exeButton = Qt.QPushButton()
            self.exeButton.setFixedSize(50, 50)
            if darkdetect.isDark():
                self.exeButton.setIcon(QtGui.QIcon("assets\\dark\\folder.png"))
            else:
                self.exeButton.setIcon(QtGui.QIcon("assets\\light\\folder.png"))
            self.exeButton.setIconSize(QtCore.QSize(35, 35))
            self.exeLayout.addWidget(self.exeButton)
            self.exeLayout.addStretch()

            self.bannerWidget = Qt.QWidget()
            self.bannerLayout = Qt.QHBoxLayout()
            self.bannerWidget.setLayout(self.bannerLayout)
            self.rightLayout.addWidget(self.bannerWidget)

            self.bannerButton = Qt.QPushButton(text="Select game banner")
            self.bannerButton.setFixedHeight(50)
            self.bannerButton.setFont(QtGui.QFont("Arial", 20))
            self.bannerLayout.addWidget(self.bannerButton)
            self.bannerLayout.addStretch()

            self.validationWidget = Qt.QWidget()
            self.validationLayout = Qt.QHBoxLayout()
            self.validationWidget.setLayout(self.validationLayout)
            self.rightLayout.addWidget(self.validationWidget)

            self.doneButton = Qt.QPushButton(text="Done")
            self.doneButton.setFixedHeight(50)
            self.doneButton.setFont(QtGui.QFont("Arial", 20))
            self.doneButton.setStyleSheet("color: green;")
            self.validationLayout.addWidget(self.doneButton)

            self.cancelButton = Qt.QPushButton(text="Cancel")
            self.cancelButton.setFixedHeight(50)
            self.cancelButton.setFont(QtGui.QFont("Arial", 20))
            self.validationLayout.addWidget(self.cancelButton)
            self.validationLayout.addStretch()
        
        def setup(self):
            """Setup every widget"""
            self.nameInput.textEdited.connect(self.updateName)
            self.folderInput.textEdited.connect(self.updateFolder)
            self.folderButton.clicked.connect(self.selectFolder)
            self.exeInput.textEdited.connect(self.updateExe)
            self.exeButton.clicked.connect(self.selectExe)
            self.bannerButton.clicked.connect(self.askBanner)
            self.cancelButton.clicked.connect(self.cancel)
            self.doneButton.clicked.connect(self.done)
        
        def selectFolder(self):
            """Select the game folder"""
            folderPath = filedialog.askdirectory(title="Select game folder")
            if folderPath:
                self.data["folder"] = folderPath.replace("/", "\\")
                if self.gameName == self.defaultName or not self.gameName:
                    self.nameInput.setText(self.data["folder"].split("\\")[-1])
                    self.updateName()
                self.folderInput.setText(self.data["folder"])
        
        def updateFolder(self):
            """Update game folder"""
            self.data["folder"] = self.folderInput.text().replace("/", "\\")

        def selectExe(self):
            """Select the game executable"""
            exePath = filedialog.askopenfilename(filetypes=(("application", "*.exe"),("all", "*.*")), initialdir=self.data["folder"], title="Select game executable")
            if exePath:
                self.data["exe"] = exePath.replace("/", "\\")
                self.exeInput.setText(self.data["exe"])
                self.pathLabel.setText(self.data["exe"].replace("\\", "\\ "))
        
        def updateExe(self):
            """Updates executable path"""
            self.data["exe"] = self.exeInput.text().replace("/", "\\")
            self.pathLabel.setText(self.data["exe"].replace("\\", "\\ "))
        
        def updateName(self):
            """Updates the game name"""
            self.gameName = self.nameInput.text()
            self.nameLabel.setText(self.gameName)
        
        def askBanner(self):
            """Asks for an image file as a banner"""
            self.bannerPath = filedialog.askopenfilename(filetypes=(("image", "*.png *.jpg *.jpeg *.webp"),("all", "*.*")), initialdir=self.data["folder"], title="Select game image banner")
            if self.bannerPath:
                # cropping the banner image
                bannerImage = Image.open(self.bannerPath)
                bannerImage = self.cropBanner(bannerImage)
                bannerImage.save("banners\\banner.png")
                self.bannerImage.setPixmap(QtGui.QPixmap("banners\\banner.png").scaled(self.bannerX, self.bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        def cropBanner(self, image:ImageFile) -> ImageFile:
            """Crops an image in banner format"""
            width, height = image.size
            currentRatio = width / height
            ratio = IGameLauncher.GameTile.ratio
            if currentRatio > ratio:
                newWidth = round(height * ratio)
                left = (width - newWidth) // 2
                right = left + newWidth
                image = image.crop((left, 0, right, height))
            elif currentRatio < ratio:
                newHeight = round(width / ratio)
                top = (height - newHeight) // 2
                bottom = top + newHeight
                image = image.crop((0, top, width, bottom))
            image = image.resize((IGameLauncher.GameTile.bigSize[0], IGameLauncher.GameTile.bigSize[1]))
            return image
        
        def cancel(self):
            """Cancels adding the game"""
            if os.path.exists("banners\\banner.png"):
                os.remove("banners\\banner.png")
        
        def done(self):
            """When the done button is clicked"""
            if os.path.exists("banners\\banner.png"):
                os.rename("banners\\banner.png", f"banners\\{self.gameName}.png")
    

    class GameTile(Qt.QWidget):
        """Object that represents a tile to display the game"""
        size = (240, 350)
        bigSize = (round(size[0]*1.5), round(size[1]*1.5))
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
                if darkdetect.isDark():
                    self.icon = QtGui.QIcon("assets\\dark\\banner.png")
                else:
                    self.icon = QtGui.QIcon("assets\\light\\banner.png")
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
        """Reads the session data, or creates an empty file, also creates banners folder if not found"""
        if not os.path.exists("data.json"):
            with open("data.json", "w", encoding="utf-8") as dataFile:
                json.dump({}, dataFile, indent=4)
        with open("data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
        if not os.path.exists("banners"):
            os.mkdir("banners")
    
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
        self.nbColumns = int(Qt.QApplication.desktop().screenGeometry().width() / ((self.GameTile.size[0] + 26)))  # number of columns for the tiles
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
        self.scrollLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
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
        if darkdetect.isDark():
            self.addButton.setIcon(QtGui.QIcon("assets\\dark\\add.png"))
        else:
            self.addButton.setIcon(QtGui.QIcon("assets\\light\\add.png"))
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
        self.scrollLayout.setAlignment(QtCore.Qt.AlignLeft)

        bannerX, bannerY = self.GameTile.bigSize[0], self.GameTile.bigSize[1]
        self.bannerImage = Qt.QLabel()
        self.bannerImage.setFixedSize(bannerX, bannerY)
        if os.path.exists(f"banners\\{gameName}.png"):
            self.bannerImage.setPixmap(QtGui.QPixmap(f"banners\\{gameName}.png").scaled(bannerX, bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.bannerImage.setPixmap(QtGui.QPixmap("assets\\light\\banner.png").scaled(bannerX, bannerY, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.infosLayout.addWidget(self.bannerImage)

        self.nameLabel = Qt.QLabel(text=gameName)
        self.nameLabel.setFont(QtGui.QFont("Arial", 32))
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setWordWrap(True)
        self.infosLayout.addWidget(self.nameLabel)

        path = self.data[gameName]["exe"]
        if path:
            self.pathLabel = Qt.QLabel(text=path.replace("\\", "\\ "))
        else:
            self.pathLabel = Qt.QLabel()
        self.pathLabel.setFont(QtGui.QFont("Arial", 16))
        self.pathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pathLabel.setWordWrap(True)
        self.infosLayout.addWidget(self.pathLabel)

        self.playButton = Qt.QPushButton(text="PLAY")
        self.playButton.setFont(QtGui.QFont("Arial", 24))
        self.playButton.setFixedHeight(60)
        self.infosLayout.addWidget(self.playButton)
        self.playButton.clicked.connect(lambda: self.launchGame(self.data[gameName]["exe"]))

        self.buildEditLayout(gameName)

    def buildEditLayout(self, gameName:str):
        """Builds the layout with the game editing options"""
        self.changeNameWidget = Qt.QWidget()
        self.changeNameLayout = Qt.QHBoxLayout()
        self.changeNameWidget.setLayout(self.changeNameLayout)
        self.modifyLayout.addWidget(self.changeNameWidget)

        self.changeNameLabel = Qt.QLabel(text="Game name:")
        self.changeNameLabel.setFont(QtGui.QFont("Arial", 24))
        self.changeNameLayout.addWidget(self.changeNameLabel)

        self.changeNameInput = Qt.QLineEdit()
        self.changeNameInput.setPlaceholderText("Game name")
        self.changeNameInput.setText(gameName)
        self.changeNameInput.setFont(QtGui.QFont("Arial", 20))
        self.changeNameInput.setFixedHeight(50)
        self.changeNameLayout.addWidget(self.changeNameInput)

        self.changeNameLayout.addStretch()

        self.folderWidget = Qt.QWidget()
        self.folderLayout = Qt.QHBoxLayout()
        self.folderWidget.setLayout(self.folderLayout)
        self.modifyLayout.addWidget(self.folderWidget)

        self.folderLabel = Qt.QLabel(text="Folder path:")
        self.folderLabel.setFont(QtGui.QFont("Arial", 24))
        self.folderLayout.addWidget(self.folderLabel)

        self.folderInput = Qt.QLineEdit()
        self.folderInput.setPlaceholderText("Folder path")
        self.folderInput.setText(self.data[gameName]["folder"])
        self.folderInput.setFont(QtGui.QFont("Arial", 20))
        self.folderInput.setFixedHeight(50)
        self.folderLayout.addWidget(self.folderInput)

        self.folderButton = Qt.QPushButton()
        self.folderButton.setFixedSize(50, 50)
        if darkdetect.isDark():
            self.folderButton.setIcon(QtGui.QIcon("assets\\dark\\folder.png"))
        else:
            self.folderButton.setIcon(QtGui.QIcon("assets\\light\\folder.png"))
        self.folderButton.setIconSize(QtCore.QSize(35, 35))
        self.folderLayout.addWidget(self.folderButton)

        self.folderLayout.addStretch()

        self.exeWidget = Qt.QWidget()
        self.exeLayout = Qt.QHBoxLayout()
        self.exeWidget.setLayout(self.exeLayout)
        self.modifyLayout.addWidget(self.exeWidget)

        self.exeLabel = Qt.QLabel(text="Executable path:")
        self.exeLabel.setFont(QtGui.QFont("Arial", 24))
        self.exeLayout.addWidget(self.exeLabel)

        self.exeInput = Qt.QLineEdit()
        self.exeInput.setPlaceholderText("exe path")
        self.exeInput.setText(self.data[gameName]["exe"])
        self.exeInput.setFont(QtGui.QFont("Arial", 20))
        self.exeInput.setFixedHeight(50)
        self.exeLayout.addWidget(self.exeInput)

        self.exeButton = Qt.QPushButton()
        self.exeButton.setFixedSize(50, 50)
        if darkdetect.isDark():
            self.exeButton.setIcon(QtGui.QIcon("assets\\dark\\folder.png"))
        else:
            self.exeButton.setIcon(QtGui.QIcon("assets\\light\\folder.png"))
        self.exeButton.setIconSize(QtCore.QSize(35, 35))
        self.exeLayout.addWidget(self.exeButton)

        self.exeLayout.addStretch()

        self.bannerWidget = Qt.QWidget()
        self.bannerLayout = Qt.QHBoxLayout()
        self.bannerWidget.setLayout(self.bannerLayout)
        self.modifyLayout.addWidget(self.bannerWidget)

        self.bannerButton = Qt.QPushButton(text="Change banner image")
        self.bannerButton.setFont(QtGui.QFont("Arial", 20))
        self.bannerButton.setFixedHeight(50)
        self.bannerLayout.addWidget(self.bannerButton)
        self.bannerLayout.addStretch()

        self.shortcutWidget = Qt.QWidget()
        self.shortcutLayout = Qt.QHBoxLayout()
        self.shortcutWidget.setLayout(self.shortcutLayout)
        self.modifyLayout.addWidget(self.shortcutWidget)

        self.shortcutButton = Qt.QPushButton(text="Add desktop shortcut")
        self.shortcutButton.setFont(QtGui.QFont("Arial", 20))
        self.shortcutButton.setFixedHeight(50)
        self.shortcutLayout.addWidget(self.shortcutButton)
        self.shortcutLayout.addStretch()

        self.removeWidget = Qt.QWidget()
        self.removeLayout = Qt.QHBoxLayout()
        self.removeWidget.setLayout(self.removeLayout)
        self.modifyLayout.addWidget(self.removeWidget)

        self.removeButton = Qt.QPushButton(text="Remove game from library")
        self.removeButton.setStyleSheet("color: red;")
        self.removeButton.setFont(QtGui.QFont("Arial", 20))
        self.removeButton.setFixedHeight(50)
        self.removeLayout.addWidget(self.removeButton)
        self.removeLayout.addStretch()

        self.finishWidget = Qt.QWidget()
        self.finishLayout = Qt.QHBoxLayout()
        self.finishWidget.setLayout(self.finishLayout)
        self.modifyLayout.addWidget(self.finishWidget)

        self.applyButton = Qt.QPushButton(text="Apply")
        self.applyButton.setStyleSheet("color: green;")
        self.applyButton.setFont(QtGui.QFont("Arial", 20))
        self.applyButton.setFixedHeight(50)
        self.finishLayout.addWidget(self.applyButton)

        self.cancelButton = Qt.QPushButton(text="Cancel")
        self.cancelButton.setFont(QtGui.QFont("Arial", 20))
        self.cancelButton.setFixedHeight(50)
        self.finishLayout.addWidget(self.cancelButton)

        self.finishLayout.addStretch()

        self.monitorEdit(gameName)
    
    def monitorEdit(self, gameName:str):
        """Connects widgets from the edit menu"""
        def updateName():
            self.modifiedData["name"] = self.changeNameInput.text()
            self.nameLabel.setText(self.modifiedData["name"])

        def updateFolder():
            self.modifiedData["folder"] = self.folderInput.text()

        def askFolder():
            newFolder = filedialog.askdirectory(title="Select game folder")
            if newFolder:
                newFolder = newFolder.replace("/", "\\")
                self.modifiedData["folder"] = newFolder
                self.folderInput.setText(newFolder)

        def updateExe():
            self.modifiedData["exe"] = self.exeInput.text()

        def askExe():
            newExe = filedialog.askopenfilename(filetypes=(("application", "*.exe"),("all", "*.*")), initialdir=self.modifiedData["folder"], title="Select game executable")
            if newExe:
                newExe = newExe.replace("/", "\\")
                self.modifiedData["exe"] = newExe
                self.exeInput.setText(newExe)
                self.pathLabel.setText(self.modifiedData["exe"].replace("\\", "\\ "))

        def updateBanner():
            newBannerPath = filedialog.askopenfilename(filetypes=(("image", "*.png *.jpg *.jpeg *.webp"),("all", "*.*")), initialdir=self.modifiedData["folder"], title="Select game image banner")
            if newBannerPath:
                self.modifiedData["newBanner"] = True
                newBanner = Image.open(newBannerPath)
                newBanner = self.AddWidget.cropBanner(self, newBanner)
                newBanner.save("banners\\banner.png")
                self.bannerImage.setPixmap(QtGui.QPixmap("banners\\banner.png").scaled(self.GameTile.bigSize[0], self.GameTile.bigSize[1], QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        def shortcut():
            self.modifiedData["createShortcut"] = True

        def remove():
            if os.path.exists(f"banners\\{gameName}.png"):
                os.remove(f"banners\\{gameName}.png")
            del(self.data[gameName])
            self.writeData()
            self.reload()

        def cancel():
            if os.path.exists("banners\\banner.png"):
                os.remove("banners\\banner.png")
            self.reload()

        def apply():
            if self.modifiedData["name"] != gameName:
                if os.path.exists(f"banners\\{gameName}.png"):
                    os.rename(f"banners\\{gameName}.png", f"banners\\{self.modifiedData["name"]}.png")
                oldData = self.data[gameName]
                del(self.data[gameName])
                self.data[self.modifiedData["name"]] = oldData
            if self.modifiedData["newBanner"]:
                if os.path.exists(f"banners\\{self.modifiedData["name"]}.png"):
                    os.remove(f"banners\\{self.modifiedData["name"]}.png")
                os.rename("banners\\banner.png", f"banners\\{self.modifiedData["name"]}.png")
            self.data[self.modifiedData["name"]]["folder"] = self.modifiedData["folder"]
            self.data[self.modifiedData["name"]]["exe"] = self.modifiedData["exe"]
            if self.modifiedData["createShortcut"]:
                pyshortcuts.make_shortcut(script=self.modifiedData["exe"], executable=self.modifiedData["exe"], name=self.modifiedData["name"], working_dir="\\".join(self.modifiedData["exe"].split("\\")[:-1]), desktop=True, startmenu=False, icon=self.modifiedData["exe"])
            self.writeData()
            self.reload()
        
        self.modifiedData = {"name":gameName, "folder":self.data[gameName]["folder"], "exe":self.data[gameName]["exe"], "newBanner":False, "createShortcut":False}
        self.changeNameInput.textEdited.connect(updateName)
        self.folderInput.textEdited.connect(updateFolder)
        self.folderButton.clicked.connect(askFolder)
        self.exeInput.textEdited.connect(updateExe)
        self.exeButton.clicked.connect(askExe)
        self.bannerButton.clicked.connect(updateBanner)
        self.shortcutButton.clicked.connect(shortcut)
        self.removeButton.clicked.connect(remove)
        self.cancelButton.clicked.connect(cancel)
        self.applyButton.clicked.connect(apply)
    
    def askGame(self):
        """Asks to add a new game"""
        self.askWidget = self.AddWidget()
        self.clear(self.scrollLayout)
        self.scrollLayout.addWidget(self.askWidget)
        self.askWidget.doneButton.clicked.connect(lambda: self.addGame(self.askWidget.gameName, self.askWidget.data))
        self.askWidget.cancelButton.clicked.connect(self.reload)

    def addGame(self, name:str, data:dict):
        """Adds a new game to the library and go to main menu"""
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
    # set style and theme
    App.setStyle("fusion")  # set theme
    if darkdetect.isDark():  # if using dark mode
        # dark mode style found online
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        App.setPalette(palette)

    Window = IGameLauncher()  # creating the GUI
    Window.start()  # starting the GUI
    App.exec_()  # executing the app
