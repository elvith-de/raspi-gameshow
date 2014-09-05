import pygame
import os.path
from pygame.locals import USEREVENT

class SoundObject(object):
    """description of class"""

    isAvailable = False
    buzzer=None
    win=None
    fail=None
    musicLoaded = False


    def __init__(self, appdirectory):
        config = pygame.mixer.get_init()
        if config is not None:
            print "Using sound parameters", config
            print "channels: ",pygame.mixer.get_num_channels()
            self.buzzer = pygame.mixer.Sound(os.path.join(appdirectory,"data","res","244932__kwahmah-02__short-buzzer.wav"))
            self.win = pygame.mixer.Sound(os.path.join(appdirectory,"data","res","171670__fins__success-2-mono.wav"))
            self.fail = pygame.mixer.Sound(os.path.join(appdirectory,"data","res","186896__mrmacross__negativebuzz.wav"))
            self.isAvailable = True
        else:
            print "Warning: pygame.mixer not available, sound not available"

    def playBuzzer(self):
        if self.isAvailable:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            self.buzzer.play()

    def playWin(self):
        if self.isAvailable:
            self.win.play()

    def playFail(self):
        if self.isAvailable:
            self.fail.play()

    def resetGameObjectSound(self):
        if self.musicLoaded:
            pygame.mixer.music.stop()
        self.musicLoaded = False

    def playGameObjectSound(self,sound):
        if self.isAvailable:
            if not self.musicLoaded:
                print sound
                pygame.mixer.music.load(sound)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(USEREVENT+3)
                self.musicLoaded = True
            else:
                pygame.mixer.music.unpause()
    def pauseGameObjectSound(self):
        if self.isAvailable:
            if self.musicLoaded:
                pygame.mixer.music.unpause()
