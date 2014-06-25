import pygame
from pygame.locals import *
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
        pygame.time.set_timer(USEREVENT+1,2000)
        super(LoaderGameObject,self).initialize()

    def update(self,time,events):
        self.gameManager.drawHUD = False
        for event in events:
            if event.type == USEREVENT+1:
                self.gameManager.setActualGameObject(ButtonCheckGameObject())

        
    def draw(self,screen):
        screen.blit(self.background,(0,0))

class ButtonCheckGameObject(GameObject):
    background = None
    font = None
    button = 0
    text = "press buzzer"
    color = (0,0,0)
    textColor = (255,255,255)

    def __init__(self):
        return super(ButtonCheckGameObject, self).__init__()

    def draw(self,screen):
        size = self.font.size(self.text)
        textSf = self.font.render(self.text,True,self.textColor).convert_alpha()
        self.background.fill(self.color)
        self.background.blit(textSf,((1024-size[0])/2,(768-size[1])/2))
        screen.blit(self.background,(0,0))
        super(ButtonCheckGameObject, self).draw(screen)

    def update(self, time,events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_1:
                self.text = "Player 1"
                self.color = (0,0,255)
                self.textColor = (255,255,255)
                pygame.time.set_timer(USEREVENT+1,2000)
                self.gameManager.hud.set_score(0,self.gameManager.hud.get_score(0)+128)
                self.gameManager.hud.set_bo5score(0,self.gameManager.hud.get_bo5score(0)+1)
            elif event.type == KEYDOWN and event.key == K_2:
                self.text = "Player 2"
                self.color = (255,255,0)
                self.textColor = (0,0,0)
                pygame.time.set_timer(USEREVENT+1,2000)
                self.gameManager.hud.set_score(1,self.gameManager.hud.get_score(1)+128)
                self.gameManager.hud.set_bo5score(1,self.gameManager.hud.get_bo5score(1)+1)
            elif event.type == USEREVENT+1:
                self.text = "press buzzer"
                self.color = (0,0,0)
                self.textColor = (255,255,255)
                self.gameManager.buttonHandler.unlock()
        super(ButtonCheckGameObject, self).update(time,events)
        
    def initialize(self):
        self.gameManager.drawHUD = True
        self.gameManager.hud.reset_values(True,True)
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill(self.color)
        self.font = pygame.font.Font(pygame.font.get_default_font(),45)
        super(ButtonCheckGameObject, self).initialize()