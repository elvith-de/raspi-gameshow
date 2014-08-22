import GameData
import sys
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

class GameStateSaver(object):
    menu = None
    lastPlayerWon = None #[0,1,Draw]
    lastGame = None #[x,y]
    menuGameData = None
    gameData = []
    categoryLock = [[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False]]
    lockByPlayer = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]

    score_blue = 0
    score_yellow = 0

    restore_from_savefile = True
    savefile = None
    appdir = None
    gameFile = None
    gameFilePath = None

    def restoreFromSaveFile(self):
        tree = ET.parse(self.savefile)
        root = tree.getroot()
        if float(root.attrib['file-format-version']) > 1.0:
            print "Error: save file has newer version than program version!"
            raise ValueError("File version of save file newer than program version")
        
        tag = root.find("lastPlayerWon")
        if tag.attrib['value'] != "None":
            if tag.attrib['value'] == "Draw":
                self.lastPlayerWon = tag.attrib['value']
            else:
                self.lastPlayerWon = int(tag.attrib['value'])
        
        tag = root.find("lastGame")
        if tag.attrib['x'] != "None" and tag.attrib['y'] != "None":
            x = int(tag.attrib['x'])
            y = int(tag.attrib['y'])
            self.lastGame = [x,y]

        tag = root.find("scoreBlue")
        self.score_blue = int(tag.attrib['value'])

        tag = root.find("scoreYellow")
        self.score_yellow = int(tag.attrib['value'])
        
        columns = root.findall("./gameLock/column")
        for col in range(5):
            rows = columns[col].findall("./row")
            for row in range(5):
                lockedBy = rows[row].attrib['player']
                if lockedBy != "-1":
                    self.categoryLock[col][row] = True
                    if lockedBy == "Draw":
                        self.lockByPlayer[col][row] = lockedBy
                    else:
                        self.lockByPlayer[col][row] = int(lockedBy)



    def __init__(self):
        for i in range(1,len(sys.argv)):
            if sys.argv[i] == "--new-game":
                self.restore_from_savefile = False
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
            print "python raspi_gameshow.py <file to load game from> [--new-game]"
            raise ValueError("unparseable arguments given")

        self.gameFilePath = os.path.abspath(os.path.dirname(self.gameFile))
        filename = os.path.split(self.gameFile)[1][:-4]+".save"+".xml"
        self.savefile = os.path.abspath(os.path.join(self.gameFilePath,filename))
        if not self.gameFilePath or not self.savefile:
            print "Error: Cannot determine path to game file or save file! Wrong arguments?"
            print "Sytax is"
            print "python raspi_gameshow.py <file to load game from> [--new-game]"
            raise ValueError("unparseable arguments given")

        if not os.path.exists(self.gameFile) or not os.path.isfile(self.gameFile):
            print "Error: game file doesn't seem to exist..."
            raise ValueError("No such file", self.gameFile)

        if self.restore_from_savefile:
            self.restore_from_savefile =  os.path.exists(self.savefile) and os.path.isfile(self.savefile)
        
        print "Config"
        print "======"
        print "appdir:",self.appdir
        print "gameFile",self.gameFile
        print "gameFilePath",self.gameFilePath
        print "restore savegame",self.restore_from_savefile
        print "savegame",self.savefile

        if self.restore_from_savefile:
            self.restoreFromSaveFile()

        

    def buildSaveStructure(self):
        root = ET.Element('raspi-gameshow-save',{'file-format-version':'1.0'})
        if self.lastPlayerWon is not None:
            ET.SubElement(root,"lastPlayerWon",{'value':str(self.lastPlayerWon)})
        else:
            ET.SubElement(root,"lastPlayerWon",{'value':'None'})
        if self.lastGame is not None:
            ET.SubElement(root,"lastGame",{'x':str(self.lastGame[0]), 'y':str(self.lastGame[1])})
        else:
            ET.SubElement(root,"lastGame",{'x':'None', 'y':'None'})
        ET.SubElement(root,"scoreBlue",{'value':str(self.score_blue)})
        ET.SubElement(root,"scoreYellow",{'value':str(self.score_yellow)})
        playerLockTag = ET.SubElement(root,"gameLock")
        for column in self.lockByPlayer:
            colTag = ET.SubElement(playerLockTag,"column")
            for lock in column:
                ET.SubElement(colTag,"row",{'player':str(lock)})
        
        return ET.tostring(root,encoding='utf-8')


    def save(self):
        file = open(self.savefile,'w+')
        xml = parseString(self.buildSaveStructure())
        file.write(xml.toprettyxml())
        file.close()
        
        #pass
        
        #todo

