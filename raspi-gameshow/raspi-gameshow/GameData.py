class GameData(object):
    """description of class"""

    image = None
    score = 0
    type = "GameData"

    def __init__(self,image,score,type):
        self.image = image
        self.score = score
        self.type = type
        return super(GameData, self).__init__()

class MenuGameData(GameData):
    categories = None

    def __init__(self, categoryList,image,score):
        self.categories = categoryList
        return super(MenuGameData, self).__init__(image,score,"MenuGameData")

class SingleImageGameData(GameData):

    def __init__(self,image,score):
        return super(SingleImageGameData, self).__init__(image,score,"SingleImageGameData")

class SoundGameData(GameData):

    sound = None

    def __init__(self,sound,image,score):
        self.sound = sound
        return super(SoundGameData, self).__init__(image,score,"SoundGameData")



class WhoIsLyingGameData(GameData):

    quote = None
    answerList = None
    answerKey = None

    def __init__(self,quote,answerList,answerKey,image,score):
        self.quote = quote
        self.answerKey = answerKey
        self.answerList = answerList
        return super(WhoIsLyingGameData, self).__init__(image,score,"WhoIsLyingGameData")


class ImageRevealGameData(GameData):

    def __init__(self,image,score):
        return super(ImageRevealGameData, self).__init__(image,score,"ImageRevealGameData")
