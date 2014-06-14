import pygame
from pygame.locals import *

class ButtonHandler(object):

    piFaceManager = None

    isLocked = False
    lockedButton = None

    def unlock(self):
        self.isLocked = False
        self.lockedButton = None
        self.piFaceManager.setPlayerButtonColor(0,"off", False)

    def pressed(self,pin_num):
        if pin_num == 2 and self.isLocked:
            self.unlock()
            event = pygame.event.Event(KEYDOWN,scancode=4,key=51,unicode=u'3', mod=4096)
            pygame.event.post(event)
        elif not self.isLocked and pin_num < 2:
            self.isLocked = True
            self.lockedButton = pin_num
            self.piFaceManager.setPlayerButtonColor(pin_num,"white",False)
            event = None
            if pin_num == 0:
                event = pygame.event.Event(KEYDOWN,scancode=2,key=49,unicode=u'1', mod=4096)
            elif pin_num == 1:
                event = pygame.event.Event(KEYDOWN,scancode=3,key=50,unicode=u'2', mod=4096)
            pygame.event.post(event)

    def setPiFaceManager(self,piFaceManager):
        self.piFaceManager = piFaceManager
        
    def __init__(self):
        return super(ButtonHandler, self).__init__()




