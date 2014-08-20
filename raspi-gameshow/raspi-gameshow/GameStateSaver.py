import GameData
import sys
import os

class GameStateSaver(object):
    menu = None
    lastPlayerWon = None #[0,1,Draw]
    lastGame = None #[x,y]
    menuGameData = None
    gameData = []

    restore_from_savefile = False
    savefile = None
    appdir = None
    gameFile = None
    gameFilePath = None

    def __init__(self):
        for i in range(1,len(sys.argv)):
            if sys.argv[i] == "--restore":
                self.restore_from_savefile = True
            else:
                self.gameFile = os.path.abspath(sys.argv[i])
        appdir = __file__
        if not appdir:
            raise ValueError
        self.appdir = os.path.abspath(os.path.dirname(__file__))
        gameFilePath = self.gameFile
        if not self.gameFile or not gameFilePath:
            print "Error: unparseable arguments given!"
            print "Sytax is"
            print "python raspi_gameshow.py <file to load game from> [--restore]"
            raise ValueError("unparseable arguments given")

        self.gameFilePath = os.path.abspath(os.path.dirname(self.gameFile))
        self.savefile = os.path.abspath(os.path.join(gameFilePath,"game.save"))
        if not self.gameFilePath or not self.savefile:
            print "Error: Cannot determine path to game file or save file! Wrong arguments?"
            print "Sytax is"
            print "python raspi_gameshow.py <file to load game from> [--restore]"
            raise ValueError("unparseable arguments given")

        
        print "Config"
        print "======"
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
