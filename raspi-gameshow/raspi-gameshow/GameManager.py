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
    gameState = None
    needQuit = False
    sound = None

    def __init__(self,initialGameObject,targetFPS,buttonHandler,piFaceManager, test=False):
        if test:
            self.initializeTest()
        else:
            self.gameState = GameStateSaver.GameStateSaver()
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
        self.piFaceManager.setPlayerButtonColor(0,"off")
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
        self.screen = pygame.display.set_mode((1024,768),pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
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

    def initializeTest(self):
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

        font = pygame.font.Font(pygame.font.get_default_font(),45)
        size = font.size("OK")
        r=0
        g=0
        b=255
        tor = True
        tog = False
        tob = False

        while 1:
                if tor:
                    r+=1
                    b-=1
                    if b==0:
                        tor=False
                        tog=True
                if tog:
                    g+=1
                    r-=1
                    if r==0:
                        tog=False
                        tob=True
                if tob:
                    b+=1
                    g-=1
                    if g==0:
                        tob=False
                        tor=True
                currentMillis = self.clock.tick(self.targetFPS)
                events = pygame.event.get()
                self.buffer.fill((r, g, b))
                self.buffer.blit(font.render("OK",True,(255,255,255)),((1024-size[0])/2,(768-size[1])/2))
                self.screen.blit(self.buffer, (0, 0))
                pygame.display.flip()

        #Handle Input Events - FOR TESTING ONLY - Events have to be checked by the GameObjects...
                for event in events:
                    if event.type == QUIT:
                        pygame.display.quit()
                        return
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        pygame.display.quit()
                        return
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