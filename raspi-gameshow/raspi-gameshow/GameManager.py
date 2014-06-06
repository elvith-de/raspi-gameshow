import pygame
from pygame.locals import *
import time


current_milli_time = lambda: int(round(time.time() * 1000))

class GameManager(object):
    screen = None
    gameObject = None
    targetFPS = 60
    clock = None


    def __init__(self,initialGameObject,targetFPS):
        self.gameObject = initialGameObject
        self.targetFPS = targetFPS
        self.initialize()
        return super(GameManager, self).__init__()

    def setActualGameObject(self,gameObject):
        if not gameObject.initialized:
            gameObject.initialize()
        self.gameObject = gameObject

    def update(self,time):
        self.gameObject.update(time)

    def draw(self):
        self.gameObject.draw()

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768),pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
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

    def run(self):
        currentMillis = 0
        lastRun = current_milli_time()
        actRun = current_milli_time()
        while 1:
            self.clock.tick(self.targetFPS)
            actRun = current_milli_time()
            currentMillis = actRun - lastRun
            lastRun = actRun
            self.update(currentMillis)
            self.draw()
        #Handle Input Events - FOR TESTING ONLY - Events have to be checked by the GameObjects...
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.display.quit()
                    return