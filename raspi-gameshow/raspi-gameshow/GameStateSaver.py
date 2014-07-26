import GameData

class GameStateSaver(object):
    menu = None
    lastPlayerWon = None
    lastGame = None
    menuGameData = None
    gameData = []

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
