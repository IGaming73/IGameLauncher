import PyQt5.QtWidgets as Qt  # interface
import os  # os interaction
import glob  # file listing
import sys  # system functions
import json  # handle json data
from tkinter import filedialog  # file choosing ui


class IGameLauncher(Qt.QMainWindow):
    """Main UI for the game launcher app"""

    class GameTile(Qt.QWidget):
        """Object that represents a tile to display the game"""

        def __init__(self, gameName:str):
            """Builds a tile for a given game"""
            #TODO
            pass


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
                json.dump({}, dataFile, indent=4)
        with open("data.json", "r", encoding="utf-8") as dataFile:
            self.data = json.load(dataFile)
    
    def buildUi(self):
        """build the UI elements"""
        #TODO
        pass


if __name__ == "__main__":  # if the file is executed directly
    App = Qt.QApplication(sys.argv)  # creating the app
    Window = IGameLauncher()  # creating the GUI
    Window.start()  # starting the GUI
    App.exec_()  # executing the app
