import pygame
from pygame.locals import *
import time
import HUD


class GameManager(object):
    screen = None
    gameObject = None
    targetFPS = 60
    clock = None
    buttonHandler = None
    hud = HUD.HUD()
    drawHUD = True
    piFaceManager = None

    def __init__(self,initialGameObject,targetFPS,buttonHandler,piFaceManager):
        self.gameObject = initialGameObject
        self.targetFPS = targetFPS
        self.buttonHandler = buttonHandler
        self.piFaceManager = piFaceManager
        self.initialize()
        return super(GameManager, self).__init__()

    def setActualGameObject(self,gameObject):
        if not gameObject.initialized:
            gameObject.gameManager = self
            gameObject.initialize()
        self.gameObject = gameObject

    def update(self,time,events):
        self.gameObject.update(time,events)
        self.hud.update(time,events)

    def draw(self):
        self.gameObject.draw(self.screen)
        if self.drawHUD:
            self.hud.draw(self.screen)

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768),pygame.DOUBLEBUF|pygame.HWSURFACE)
        pygame.mouse.set_visible(True)
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250, 0, 250))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        print "Using driver",pygame.display.get_driver()
        print "Set SDL_VIDEODRIVER to change"
        print "-----------------------------"
        print "Driver Info:"
        print pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.hud.initialize()

    def run(self):
        while 1:
            currentMillis = self.clock.tick(self.targetFPS)
            events = pygame.event.get()
            self.update(currentMillis,events)
            self.draw()
            pygame.display.flip()

        #Handle Input Events - FOR TESTING ONLY - Events have to be checked by the GameObjects...
            for event in events:
                if event.type == QUIT:
                    pygame.display.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.display.quit()
                    return