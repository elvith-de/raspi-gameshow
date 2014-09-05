import threading
import GameData
import xml.etree.ElementTree as ET
import os

class GameFileLoader(threading.Thread):
    """description of class"""

    file = None
    loader = None

    gameState = None
    datafile = None
    dataPath = None
    restore = None
    saveFile = None

    def __init__(self,loaderGameObject):
        self.loader = loaderGameObject
        return super(GameFileLoader,self).__init__(name="XMLLoader")

    def checkVersion(self,ver):
        version = float(ver)
        if version > 1.0:
            import time
            self.loader.setText("Fehler: falsches Dateiformat")
            time.sleep(30)
            self.loader.gameManager.needQuit = True


    def parse(self,game):
        type = game.attrib["type"]
        score = int(game.attrib["score"])
        if type == "SingleImage":
            img = game.find("./img")
            image = img.attrib["src"]
            image = os.path.join(self.dataPath,"img",image)
            return GameData.SingleImageGameData(image,score)
        elif type == "ImageReveal":
            img = game.find("./img")
            image = img.attrib["src"]
            image = os.path.join(self.dataPath,"img",image)
            return GameData.ImageRevealGameData(image,score)
        elif type == "WhoIsLying":
            quote = game.find("./quote").text
            answerlistTag = game.find("./answerList")
            answerList = []
            answerKey = []
            for answerTag in answerlistTag:
                key = True if answerTag.attrib["isLying"] == "True" else False
                answer = answerTag.text
                answerKey.append(key)
                answerList.append(answer)
            #TODO
            return GameData.WhoIsLyingGameData(quote,answerList,answerKey,None,score)
        elif type == "Sound":
            soundfile = game.find("./sound").attrib["src"]
            soundfile = os.path.join(self.dataPath,"snd",soundfile)
            image = os.path.join("data","res","music.png")
            return GameData.SoundGameData(soundfile,image,score)

    def run(self):
        try:
            self.gameState = self.loader.gameManager.gameState
            self.datafile = self.gameState.gameFile
            self.dataPath = self.gameState.gameFilePath
            self.restore = self.gameState.restore_from_savefile
            self.saveFile = self.gameState.savefile
        
            self.loader.setText("Parse Datei")
            tree = ET.parse(self.datafile)
            root = tree.getroot()
            self.checkVersion(root.attrib["file-format-version"])

            categoryNames = []
            gameData = []
            for categoryRoot in root:
                gameDataInCategory = []
                catName = categoryRoot.attrib["name"]
                self.loader.setText("Erzeuge Kategorie "+catName)
                categoryNames.append(catName)
                for i in range(5):
                    game = categoryRoot[i]
                    gameDataInCategory.append(self.parse(game))
                gameData.append(gameDataInCategory)

            self.gameState.menuGameData = GameData.MenuGameData(categoryNames,None,None)
            self.gameState.gameData = gameData
        except:
            self.loader.gameManager.needQuit = True