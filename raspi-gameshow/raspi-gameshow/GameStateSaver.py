import GameData
import sys
import os

class GameStateSaver(object):
    menu = None
    lastPlayerWon = None
    lastGame = None
    menuGameData = None
    gameData = []

    restore_from_savefile = False
    savefile = None
    appdir = None
    gameFile = None
    gameFilePath = None

    def __init__(self):
        for e in sys.argv:
            print e
            if e == "raspi_gameshow.py":
                continue
            if e == "--restore":
                self.restore_from_savefile = True
            else:
                self.gameFile = os.path.abspath(e)
        appdir = __file__
        if not appdir:
            raise ValueError
        self.appdir = os.path.abspath(os.path.dirname(__file__))
        gameFilePath = self.gameFile
        if not gameFilePath:
            raise ValueError
        self.gameFilePath = os.path.abspath(os.path.dirname(self.gameFile))
        self.savefile = os.path.abspath(os.path.join(gameFilePath,"game.save"))

        
        print "Config:"
        print "appdir:",self.appdir
        print "gameFile",self.gameFile
        print "gameFilePath",self.gameFilePath
        print "restore",self.restore_from_savefile
        print "savegame",self.savefile


    def fillDummyGameData(self):
        import os
        for cat in range(5):
            list = []
            dummyImage = os.path.join("data","test","image.png")
            list.append(GameData.SingleImageGameData(dummyImage,100))
            list.append(GameData.WhoIsLyingGameData("Ich bin ein Fussballer",
                            ["Hansjoerg","Goetze","Neuer","Anna"],
                            [True,False,False,True],dummyImage,200))
            list.append(GameData.ImageRevealGameData(dummyImage,300))
            list.append(GameData.SingleImageGameData(dummyImage,400))
            list.append(GameData.WhoIsLyingGameData("Ich bin ein Fussballer",
                            ["Hansjoerg","Goetze","Neuer","Anna"],
                            [True,False,False,True],dummyImage,500))

            self.gameData.append(list)
