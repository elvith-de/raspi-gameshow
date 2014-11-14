# -*- coding: iso-8859-15 -*-
import pygame
from pygame.locals import *
import os
import random
import GameData
import GameFileLoader


class GameObject(object):

    initialized = False
    gameManager = None
    background = None
    P1PressedSf = None
    P2PressedSf = None
    gameDrawSf = None
    showP1Pressed = False
    showP2Pressed = False
    showRight = False
    showWrong = False
    rightSf = None
    wrongSf = None
    showGameDraw = False
    objectLocked = False
    sound = None

    def __init__(self, gameData):
        return super(GameObject, self).__init__()

    def update(self,time,events):
        pass

    def draw(self,screen,callSuper=True):
        self.drawButtonPressOverlay(screen)

    def drawButtonPressOverlay(self,screen):
        if self.showP1Pressed:
            screen.blit(self.P1PressedSf,(312,234))
        elif self.showP2Pressed:
            screen.blit(self.P2PressedSf,(312,234))
        elif self.showGameDraw:
            screen.blit(self.gameDrawSf,(312,234))
        elif self.showRight:
            screen.blit(self.rightSf,(312,234))
        elif self.showWrong:
            screen.blit(self.wrongSf,(312,234))
    
    def switchedTo(self):
        pass
    
    def initialize(self):
        font = pygame.font.Font(pygame.font.get_default_font(),45)
        self.P1PressedSf = pygame.surface.Surface((400,300)).convert()
        self.P1PressedSf.fill((0,0,255))
        size = font.size("Team Blau")
        self.P1PressedSf.blit(font.render("Team Blau",True,(255,255,255)),((400-size[0])/2,(300-size[1])/2))
        self.P2PressedSf = pygame.surface.Surface((400,300)).convert()
        self.P2PressedSf.fill((255,255,0))
        size = font.size("Team Gelb")
        self.P2PressedSf.blit(font.render("Team Gelb",True,(0,0,0)),((400-size[0])/2,(300-size[1])/2))
        self.gameDrawSf = pygame.surface.Surface((400,300)).convert()
        self.gameDrawSf.fill((128,128,128))
        size = font.size("Unentschieden!")
        self.gameDrawSf.blit(font.render("Unentschieden!",True,(0,0,0)),((400-size[0])/2,(300-size[1])/2))
        self.rightSf = pygame.surface.Surface((400,300)).convert()
        self.rightSf.fill((0,255,0))
        size = font.size("Richtig!")
        self.rightSf.blit(font.render("Richtig!",True,(0,0,0)),((400-size[0])/2,(300-size[1])/2))
        self.wrongSf = pygame.surface.Surface((400,300)).convert()
        self.wrongSf.fill((255,0,0))
        size = font.size("Falsch!")
        self.wrongSf.blit(font.render("Falsch!",True,(0,0,0)),((400-size[0])/2,(300-size[1])/2))
        
        self.initialized = True

class LoaderGameObject(GameObject):
    
    loader = None
    font = None
    text = "Loading..."
    textDirty = True
    logo=None
    textSf = None
    textSfsize = None

    def setText(self,text):
        self.textDirty = True
        self.text = text

    def __init__(self, gameData):
        self.loader = GameFileLoader.GameFileLoader(self)
        return super(LoaderGameObject, self).__init__(gameData)

    def createTextSf(self):
        self.textSf = self.font.render(self.text,True,(255,255,255)).convert_alpha()
        self.textSfsize = self.font.size(self.text)
        self.textDirty = False

    def initialize(self):
        self.logo = pygame.image.load(os.path.join("data","res","logo.png")).convert()
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.font = pygame.font.Font(pygame.font.get_default_font(),45)
        self.loader.start()
        super(LoaderGameObject,self).initialize()

    def update(self,time,events):
        if self.textDirty:
            self.createTextSf()
        if not self.loader.isAlive():
                self.gameManager.gameState.menu = MenuGameObject(self.gameManager.gameState.menuGameData)
                self.gameManager.setCurrentGameObject(self.gameManager.gameState.menu)

        
    def draw(self,screen,callSuper=True):
        self.background.fill((0,0,0))
        self.background.blit(self.logo,(300,151))
        text = self.font.render("raspi-gameshow",True,(0,0,0)).convert_alpha()
        self.background.blit(text,(332,490))        
        self.background.blit(self.textSf,(((1024-self.textSfsize[0])/2,(768-self.textSfsize[1]-10))))
        screen.blit(self.background,(0,0))

    def switchedTo(self):
        self.gameManager.drawHUD = False
        self.gameManager.hud.bo5_visible = False

class ButtonCheckGameObject(GameObject):
    
    font = None
    button = 0
    text = "press buzzer"
    color = (0,0,0)
    textColor = (255,255,255)

    def __init__(self,gameData):
        return super(ButtonCheckGameObject, self).__init__(gameData)

    def draw(self,screen,callSuper=True):
        size = self.font.size(self.text)
        textSf = self.font.render(self.text,True,self.textColor).convert_alpha()
        self.background.fill(self.color)
        self.background.blit(textSf,((1024-size[0])/2,(768-size[1])/2))
        screen.blit(self.background,(0,0))
        if callSuper:
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
                self.gameManager.piFaceManager.setPlayerButtonColor(0,"blue")
            elif event.type == KEYDOWN and event.key == K_2:
                self.text = "Player 2"
                self.color = (255,255,0)
                self.textColor = (0,0,0)
                pygame.time.set_timer(USEREVENT+1,2000)
                self.gameManager.hud.set_score(1,self.gameManager.hud.get_score(1)+128)
                self.gameManager.hud.set_bo5score(1,self.gameManager.hud.get_bo5score(1)+1)
                self.gameManager.piFaceManager.setPlayerButtonColor(1,"yellow")
            elif event.type == USEREVENT+1:
                pygame.time.set_timer(USEREVENT+1,0)
                self.text = "press buzzer"
                self.color = (0,0,0)
                self.textColor = (255,255,255)
                self.gameManager.buttonHandler.unlock()
                self.gameManager.piFaceManager.setPlayerButtonColor(0,"off")
        if callSuper:
            super(ButtonCheckGameObject, self).update(time,events)
        
    def initialize(self):
        self.gameManager.hud.reset_values(True,True)
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill(self.color)
        self.font = pygame.font.Font(pygame.font.get_default_font(),45)
        super(ButtonCheckGameObject, self).initialize()

    def switchedTo(self):
        self.gameManager.drawHUD = True
        self.gameManager.hud.bo5_visible = True

class MenuGameObject(GameObject):

    
    categoryField = []
    
    categoryText = None
    categoryTextSf = []
    selectionMarker = None
    currentSelection = [0,0]
    test = (255,255,0)
    font = None
    colorField = {'Player-1':[[128,128,128],[0,0,0]],'Player0':[[0,0,255],[0,0,0]], 'Player1':[[255,255,0],[0,0,0]],'PlayerDraw':[[0,0,0],[255,255,255]]}

    def __init__(self, gameData):
        self.categoryText = gameData.categories
        return super(MenuGameObject, self).__init__(gameData)

    def get_Field_Surface(self, value, playerNum):
        key = "Player"+str(playerNum)
        colBg = self.colorField[key][0]
        colTx = self.colorField[key][1]
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
            for row in range(5):
                points = (row+1)*100
                catFields.append(self.get_Field_Surface(points,self.gameManager.gameState.lockByPlayer[cat][row]))
            self.categoryField.append(catFields)

        font2 = pygame.font.Font(pygame.font.get_default_font(),25)
        for cat in self.categoryText:

            self.categoryTextSf.append(font2.render(cat,True,(255,255,255)).convert_alpha())
        
        self.selectionMarker = pygame.surface.Surface((187,105)).convert()
        self.selectionMarker.fill((255,255,255))
        super(MenuGameObject,self).initialize()

    def update(self,time,events):
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
                if not self.gameManager.gameState.categoryLock[self.currentSelection[0]][self.currentSelection[1]]:
                    #start according gameObject
                    print "Starting",self.currentSelection
                    self.gameManager.gameState.categoryLock[self.currentSelection[0]][self.currentSelection[1]] = True
                    self.gameManager.gameState.lastGame = self.currentSelection
                    self.startGame()


    def draw(self, screen, callSuper=True):
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
        super(MenuGameObject,self).draw(screen)

    def switchedTo(self):
        self.gameManager.drawHUD = True
        self.gameManager.hud.bo5_visible = False
        if self.gameManager.gameState.lastGame != None:
            self.currentSelection = self.gameManager.gameState.lastGame
            self.categoryField[self.currentSelection[0]][self.currentSelection[1]] = self.get_Field_Surface(((self.currentSelection[1]+1)*100),self.gameManager.gameState.lastPlayerWon)
            self.gameManager.gameState.lockByPlayer[self.currentSelection[0]][self.currentSelection[1]] = self.gameManager.gameState.lastPlayerWon

    def startGame(self):
        gameData = self.gameManager.gameState.gameData[self.currentSelection[0]][self.currentSelection[1]]
        gameObject = None
        if gameData.type == "SingleImageGameData":
            gameObject = SingleImageGameObject(gameData)
        elif gameData.type == "WhoIsLyingGameData":
            gameObject = WhoIsLyingGameObject(gameData)
        elif gameData.type == "ImageRevealGameData":
            gameObject = ImageRevealGameObject(gameData)
        elif gameData.type == "SoundGameData":
            gameObject = SoundGameObject(gameData)
        else:
            print "error, type is",gameData.type
        self.gameManager.setCurrentGameObject(gameObject)

class SingleImageGameObject(GameObject):
    
    image = None
    imageSf = None
    score = 0

    def __init__(self,gameData):
        self.image = gameData.image
        self.score = gameData.score
        return super(SingleImageGameObject, self).__init__(gameData)

    def update(self,time,events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_1 and not self.objectLocked:
                self.sound.playBuzzer()
                self.showP1Pressed = True
                self.objectLocked = True
                self.gameManager.piFaceManager.setPlayerButtonColor(0,"blue")
            elif event.type == KEYDOWN and event.key == K_2 and not self.objectLocked:
                self.sound.playBuzzer()
                self.showP2Pressed = True
                self.objectLocked = True
                self.gameManager.piFaceManager.setPlayerButtonColor(1,"yellow")
            elif event.type == KEYDOWN and event.key == K_3:
                self.showP1Pressed = False
                self.showP2Pressed = False
                self.objectLocked = False
                self.gameManager.piFaceManager.setPlayerButtonColor(0,"off")
            elif event.type == KEYDOWN and event.key == K_4 and self.objectLocked:
                if self.showP1Pressed:
                    self.showP1Pressed = False
                    self.showP2Pressed = False
                    self.gameManager.hud.set_score(0,self.gameManager.hud.get_score(0)+self.score)
                    self.gameManager.gameState.lastPlayerWon = 0
                    self.showRight = True
                    self.sound.playWin()
                    self.gameManager.piFaceManager.setPlayerButtonColor(0,"green")
                    self.gameManager.piFaceManager.setPlayerButtonColor(1,"red", True)
                else:
                    self.showP1Pressed = False
                    self.showP2Pressed = False
                    self.gameManager.hud.set_score(1,self.gameManager.hud.get_score(1)+self.score)
                    self.gameManager.gameState.lastPlayerWon = 1
                    self.showRight = True
                    self.sound.playWin()
                    self.gameManager.piFaceManager.setPlayerButtonColor(0,"red")
                    self.gameManager.piFaceManager.setPlayerButtonColor(1,"green", True)
                self.showP1Pressed = False
                self.showP2Pressed = False
                pygame.time.set_timer(USEREVENT+1,1500)
            elif event.type == KEYDOWN and event.key == K_5 and self.objectLocked:
                if self.showP2Pressed:
                    self.showP1Pressed = False
                    self.showP2Pressed = False
                    self.showWrong = True
                    self.gameManager.hud.set_score(0,self.gameManager.hud.get_score(0)+self.score)
                    self.gameManager.gameState.lastPlayerWon = 0
                    self.sound.playFail()
                    self.gameManager.piFaceManager.setPlayerButtonColor(1,"red")
                    self.gameManager.piFaceManager.setPlayerButtonColor(0,"green", True)
                else:
                    self.showP1Pressed = False
                    self.showP2Pressed = False
                    self.showWrong = True
                    self.gameManager.hud.set_score(1,self.gameManager.hud.get_score(1)+self.score)
                    self.gameManager.gameState.lastPlayerWon = 1
                    self.sound.playFail()
                    self.gameManager.piFaceManager.setPlayerButtonColor(0,"red")
                    self.gameManager.piFaceManager.setPlayerButtonColor(1,"green", True)
                self.showP1Pressed = False
                self.showP2Pressed = False
                pygame.time.set_timer(USEREVENT+1,1500)
            elif event.type == USEREVENT+1:
                self.gameManager.setCurrentGameObject(self.gameManager.gameState.menu)
        super(SingleImageGameObject, self).update(time,events)


    def draw(self,screen, callSuper=True):
        screen.blit(self.background,(0,0))
        screen.blit(self.imageSf,(87,65))
        if callSuper:
            super(SingleImageGameObject, self).draw(screen)

    def initialize(self):
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill((0,0,0))
        self.imageSf = pygame.image.load(self.image).convert()
        super(SingleImageGameObject,self).initialize()

    def switchedTo(self):
        self.gameManager.drawHUD = True
        self.gameManager.hud.bo5_visible = False
        super(SingleImageGameObject, self).switchedTo()


class WhoIsLyingGameObject(GameObject):
    
    quote = None
    quoteSf = None
    answerList = None
    answerSf = None
    answerKey = None
    score = 0
    elapsedMillis = 0
    timerSf = None
    font = None
    answerNum = 0

    def __init__(self,gameData):
        self.quote = gameData.quote
        self.answerList = gameData.answerList
        self.answerKey = gameData.answerKey
        self.score = gameData.score

        return super(WhoIsLyingGameObject, self).__init__(gameData)

    def update(self,time,events):

        for event in events:
            if event.type == KEYDOWN and event.key == K_1 and not self.objectLocked:
                self.sound.playBuzzer()
                self.showP1Pressed = True
                self.objectLocked = True
                pygame.time.set_timer(USEREVENT+1,2000)
                self.gameManager.piFaceManager.setPlayerButtonColor(0,"blue")
            elif event.type == KEYDOWN and event.key == K_2 and not self.objectLocked:
                self.sound.playBuzzer()
                self.showP2Pressed = True
                self.objectLocked = True
                pygame.time.set_timer(USEREVENT+1,2000)
                self.gameManager.piFaceManager.setPlayerButtonColor(1,"yellow")
            elif event.type == USEREVENT+1:
                if self.answerKey[self.answerNum]:
                    self.showRight = True
                    self.sound.playWin()
                    if self.showP1Pressed:
                        self.gameManager.hud.set_score(0,self.score + self.gameManager.hud.get_score(0))
                        self.gameManager.gameState.lastPlayerWon = 0
                        self.gameManager.piFaceManager.setPlayerButtonColor(0,"green")
                        self.gameManager.piFaceManager.setPlayerButtonColor(1,"red",True)
                    elif self.showP2Pressed:
                        self.gameManager.hud.set_score(1,self.score + self.gameManager.hud.get_score(1))
                        self.gameManager.gameState.lastPlayerWon = 1
                        self.gameManager.piFaceManager.setPlayerButtonColor(1,"green")
                        self.gameManager.piFaceManager.setPlayerButtonColor(0,"red",True)
                else:
                    self.sound.playFail()
                    self.showWrong = True
                    if self.showP1Pressed:
                        self.gameManager.hud.set_score(1,self.score + self.gameManager.hud.get_score(1))
                        self.gameManager.gameState.lastPlayerWon = 1
                        self.gameManager.piFaceManager.setPlayerButtonColor(1,"green")
                        self.gameManager.piFaceManager.setPlayerButtonColor(0,"red",True)
                    if self.showP2Pressed:
                        self.gameManager.hud.set_score(0,self.score + self.gameManager.hud.get_score(0))
                        self.gameManager.gameState.lastPlayerWon = 0
                        self.gameManager.piFaceManager.setPlayerButtonColor(0,"green")
                        self.gameManager.piFaceManager.setPlayerButtonColor(1,"red",True)
                self.showP1Pressed = False
                self.showP2Pressed = False
                pygame.time.set_timer(USEREVENT+1,0)
                pygame.time.set_timer(USEREVENT+2,1500)
            elif event.type == USEREVENT+2:
                self.gameManager.setCurrentGameObject(self.gameManager.gameState.menu)

        
        if not self.objectLocked:
            self.elapsedMillis += time
            if self.elapsedMillis >= 5000:
                self.answerNum += 1
                if self.answerNum < len(self.answerList):
                    self.elapsedMillis = 0
                    self.answerSf = self.answerSf = self.font.render(self.answerList[self.answerNum],True,(255,255,255))
                else:
                    self.showGameDraw = True
                    self.objectLocked = True
                    self.gameManager.gameState.lastPlayerWon = "Draw"
                    pygame.time.set_timer(USEREVENT+2,1500)
        super(WhoIsLyingGameObject, self).update(time,events)


    def draw(self,screen, callSuper=True):
        screen.blit(self.background,(0,0))
        screen.blit(self.quoteSf,((1024-self.quoteSf.get_width())/2,150))
        screen.blit(self.answerSf,((1024-self.answerSf.get_width())/2,350))
        screen.blit(self.timerSf,(137,450),(0,0,750-(self.elapsedMillis/5000.*750.),50))
        if callSuper:
            super(WhoIsLyingGameObject, self).draw(screen)

    def initialize(self):
        self.background = pygame.surface.Surface((1024,768)).convert()
        self.background.fill((0,0,0))
        self.font = pygame.font.Font(pygame.font.get_default_font(),25)
        self.quoteSf = self.font.render(self.quote,True,(255,255,255))
        self.timerSf = pygame.surface.Surface((750,50)).convert()
        self.timerSf.fill((0,255,0))
        self.answerSf = self.font.render(self.answerList[self.answerNum],True,(255,255,255))
        super(WhoIsLyingGameObject,self).initialize()

    def switchedTo(self):
        self.elapsedMillis = 0
        self.answerNum = 0
        self.gameManager.drawHUD = True
        self.gameManager.hud.bo5_visible = False
        super(WhoIsLyingGameObject, self).switchedTo()

class ImageRevealGameObject(SingleImageGameObject):
    
    blackSF = None
    renderSFList = []
    
    def __init__(self,gameData):
        return super(ImageRevealGameObject, self).__init__(gameData)

    def update(self,time,events):
        for event in events:
            if event.type == USEREVENT+2:
                if len(self.renderSFList) > 0:
                    self.renderSFList.remove(self.renderSFList[0])
            elif event.type == KEYDOWN and event.key == K_1 and not self.objectLocked:
                pygame.time.set_timer(USEREVENT+2,0)
            elif event.type == KEYDOWN and event.key == K_2 and not self.objectLocked:
                pygame.time.set_timer(USEREVENT+2,0)
            elif event.type == KEYDOWN and event.key == K_3:
                pygame.time.set_timer(USEREVENT+2,700)
        if self.showRight or self.showWrong:
            if len(self.renderSFList) > 0:
                self.renderSFList = []
        super(ImageRevealGameObject, self).update(time,events)

    def draw(self,screen,callSuper=True):
        super(ImageRevealGameObject, self).draw(screen,False)
        for sfID in self.renderSFList:
            col = sfID % 12
            row = (sfID -col)/12
            screen.blit(self.blackSF,(86+(col*71),65+(row*71)))
        self.drawButtonPressOverlay(screen)
        
    def switchedTo(self):
        pygame.time.set_timer(USEREVENT+2,700)
        super(ImageRevealGameObject, self).switchedTo()
    
    def initialize(self):
        self.blackSF = pygame.surface.Surface((71,71)).convert()
        self.blackSF.fill((0,0,0))
        self.renderSFList = range(108)
        random.shuffle(self.renderSFList)
        super(ImageRevealGameObject, self).initialize()


class SoundGameObject(SingleImageGameObject):
    
    goSound = None
    
    def __init__(self,gameData):
        self.goSound = gameData.sound
        return super(SoundGameObject, self).__init__(gameData)

    def update(self,time,events):
        for event in events:
            if event.type == USEREVENT+3:
                #Draw Game
                self.showGameDraw = True
                self.gameManager.gameState.lastPlayerWon = "Draw"
                pygame.time.set_timer(USEREVENT+1,1500)
            elif event.type == KEYDOWN and event.key == K_1 and not self.objectLocked:
                self.sound.pauseGameObjectSound()
            elif event.type == KEYDOWN and event.key == K_2 and not self.objectLocked:
                self.sound.pauseGameObjectSound()
            elif event.type == KEYDOWN and event.key == K_3:
                self.sound.playGameObjectSound(self.goSound)

        super(SoundGameObject, self).update(time,events)

    def draw(self,screen,callSuper=True):
        super(SoundGameObject, self).draw(screen)
        
    def switchedTo(self):
        self.sound.playGameObjectSound(self.goSound)

    def initialize(self):
        super(SoundGameObject, self).initialize()