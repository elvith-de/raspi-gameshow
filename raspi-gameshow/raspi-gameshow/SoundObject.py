import pygame
import os.path

class SoundObject(object):
    """description of class"""

    isAvailable = False
    buzzer=None
    win=None
    fail=None


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
            pygame.mixer.stop()
            self.buzzer.play()

    def playWin(self):
        if self.isAvailable:
            pygame.mixer.stop()
            self.win.play()

    def playFail(self):
        if self.isAvailable:
            pygame.mixer.stop()
            self.fail.play()