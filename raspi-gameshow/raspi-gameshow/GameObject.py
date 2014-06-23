import pygame
import os


class GameObject(object):

    initialized = False
    gameManager = None

    def __init__(self):
        return super(GameObject, self).__init__()

    def update(self,time,events):
        pass

    def draw(self,screen):
        pass

    def initialize(self):
        self.initialized = True


class LoaderGameObject(GameObject):
    background = None
    def __init__(self):
        self.initialize()
        return super(LoaderGameObject, self).__init__()

    def initialize(self):
        logo = pygame.image.load(os.path.join("data","res","logo.png")).convert()
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill((0,0,0))
        self.background.blit(logo,(300,151))
        font = pygame.font.Font(pygame.font.get_default_font(),45)
        text = font.render("raspi-gameshow",True,(0,0,0)).convert_alpha()
        self.background.blit(text,(332,490))
        text = font.render("Loading...",True,(255,255,255)).convert_alpha()
        size = font.size("Loading...")
        self.background.blit(text,(((1024-size[0])/2,(768-size[1]-10))))
        super(LoaderGameObject,self).initialize()
    def update(self,time,events):
        self.gameManager.drawHUD = False
        pass
    def draw(self,screen):
        screen.blit(self.background,(0,0))

class WhoIsLyingGameObject(GameObject):
    def __init__(self):
        return super(SimpleQuestionGameObject, self).__init__()

    def draw(self,screen):
        super(SimpleQuestionGameObject, self).draw()

    def update(self, time,events):
        super(SimpleQuestionGameObject, self).update(time)
        self.gameManager.drawHUD = True

    def initialize(self):

        super(SimpleQuestionGameObject, self).initialize()