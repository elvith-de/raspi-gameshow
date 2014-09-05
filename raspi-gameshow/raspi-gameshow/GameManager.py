import pygame
from pygame.locals import *
import time
import HUD
import GameStateSaver
import SoundObject



class GameManager(object):
    screen = None
    buffer = None
    gameObject = None
    targetFPS = 60
    clock = None
    buttonHandler = None
    hud = HUD.HUD()
    drawHUD = True
    piFaceManager = None
    gameState = GameStateSaver.GameStateSaver()
    needQuit = False
    sound = None

    def __init__(self,initialGameObject,targetFPS,buttonHandler,piFaceManager):
        self.gameObject = initialGameObject
        self.hud.gameState = self.gameState
        self.targetFPS = targetFPS
        self.buttonHandler = buttonHandler
        self.piFaceManager = piFaceManager
        self.initialize()
        return super(GameManager, self).__init__()

    def setCurrentGameObject(self,gameObject):
        if not gameObject.initialized:
            pygame.time.set_timer(USEREVENT+1,0)
            pygame.time.set_timer(USEREVENT+2,0)
            gameObject.gameManager = self
            gameObject.initialize()
            self.buttonHandler.unlock()
        self.gameObject = gameObject
        self.gameObject.sound = self.sound
        self.sound.resetGameObjectSound()
        gameObject.switchedTo()
        self.gameState.save()

    def update(self,time,events):
        self.gameObject.update(time,events)
        self.hud.update(time,events)

    def draw(self):
        '''Draws current GameObject. 
        Since fbcon seems to have most performance on raspi but doesn't support double buffering, 
        a surface is used to simulate double buffering to prevent flickering (won't solve all problems though)'''
        self.gameObject.draw(self.buffer)
        if self.drawHUD:
            self.hud.draw(self.buffer)
        self.screen.blit(self.buffer,(0,0))

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024,768),pygame.DOUBLEBUF|pygame.HWSURFACE)
        pygame.mouse.set_visible(True)
        self.buffer = pygame.Surface(self.screen.get_size())
        self.buffer = self.buffer.convert()
        self.buffer.fill((250, 0, 250))
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()
        print "Using driver",pygame.display.get_driver()
        print "Set SDL_VIDEODRIVER to change"
        print "-----------------------------"
        print "Driver Info:"
        print pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.hud.initialize()
        self.sound = SoundObject.SoundObject(self.gameState.appdir)
        self.gameObject.sound = self.sound

    def run(self):
       # try:
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
                        self.sound.resetGameObjectSound()
                        return
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        pygame.display.quit()
                        self.sound.resetGameObjectSound()
                        return
                if self.needQuit:
                    pygame.display.quit()
                    self.sound.resetGameObjectSound()
                    return
        #except Exception as e:
         #   print e
          #  pygame.display.quit()
           # return