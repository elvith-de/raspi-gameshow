# -*- coding: iso-8859-15 -*-
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
                #self.gameManager.setActualGameObject(ButtonCheckGameObject())
                self.gameManager.setActualGameObject(MenuGameObject(["intakt","Action","Bilder","Wer lügt?","Blatest"]))

        
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
                pygame.time.set_timer(USEREVENT+1,0)
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

class MenuGameObject(GameObject):

    background = None
    categoryField = []
    categoryLock = []
    categoryText = None
    categoryTextSf = []
    selectionMarker = None
    currentSelection = [0,0]
    test = (255,255,0)
    font = None

    def __init__(self, categories):
        self.categoryText = categories
        return super(MenuGameObject, self).__init__()

    def get_Field_Surface(self, value, colBg, colTx):
        field = pygame.surface.Surface((167,85)).convert()
        field.fill(colBg)
        size = self.font.size(str(value))
        text = self.font.render(str(value),True,colTx)
        field.blit(text,((167-size[0])/2,(85-size[1])/2))
        return field

    def initialize(self):
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill((0,0,0))
        self.font = pygame.font.Font(pygame.font.get_default_font(),45)

        for cat in range(5):
            catFields = []
            catLock = []
            for row in range(100,600,100):
                catFields.append(self.get_Field_Surface(row,(128,128,128),(0,0,0)))
                catLock.append(False)
                #catFields.append(field)
            self.categoryField.append(catFields)
            self.categoryLock.append(catLock)

        font2 = pygame.font.Font(pygame.font.get_default_font(),25)
        for cat in self.categoryText:

            self.categoryTextSf.append(font2.render(cat,True,(255,255,255)).convert_alpha())
        
        self.selectionMarker = pygame.surface.Surface((187,105)).convert()
        self.selectionMarker.fill((255,255,255))
        super(MenuGameObject,self).initialize()

    def update(self,time,events):
        self.gameManager.drawHUD = True
        self.gameManager.hud.bo5_visible = False
        for event in events:
            if event.type == KEYDOWN and event.key == K_RIGHT:
                if self.currentSelection[0] < 4:
                    self.currentSelection[0] += 1
            elif event.type == KEYDOWN and event.key == K_LEFT:
                if self.currentSelection[0] > 0:
                    self.currentSelection[0] -= 1
            elif event.type == KEYDOWN and event.key == K_UP:
                if self.currentSelection[1] > 0:
                    self.currentSelection[1] -= 1
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if self.currentSelection[1] < 4:
                    self.currentSelection[1] += 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                if not self.categoryLock[self.currentSelection[0]][self.currentSelection[1]]:
                    #start according gameObject
                    print "Starting",self.currentSelection
                    if self.test == (255,255,0):
                        self.test = (0,0,255)
                    else:
                        self.test = (255,255,0)
                    self.categoryField[self.currentSelection[0]][self.currentSelection[1]] = self.get_Field_Surface(((self.currentSelection[1]+1)*100),self.test,(0,0,0))
                    self.categoryLock[self.currentSelection[0]][self.currentSelection[1]] = True

    def draw(self, screen):
        screen.blit(self.background,(0,0))
        x = 29+self.currentSelection[0]*167+self.currentSelection[0]*33 - 10
        y = 173+self.currentSelection[1]*85+self.currentSelection[1]*15 -10
        screen.blit(self.selectionMarker,(x,y))
        for col in range(5):
            x = 196+col*167+col*33
            y = 173
            size = self.categoryTextSf[col].get_size()
            offset_x = (167-size[0])/2+size[0]
            offset_y = 75
            screen.blit(self.categoryTextSf[col],(x-offset_x,y-offset_y))
            x = 29+col*167+col*33
            for row in range(5):    
                y = 173+row*85+row*15
                screen.blit(self.categoryField[col][row],(x,y))