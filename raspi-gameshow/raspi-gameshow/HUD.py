import pygame
import os

class HUD(object):
    """description of class"""

    score_blue = 0
    score_blue_dirty = True
    score_blue_img = None
    score_blue_draw = None
    score_yellow = 0
    score_yellow_dirty = True
    score_yellow_img = None
    score_yellow_draw = None
    bo5_visible = False
    bo5_blue_val = 0
    bo5_blue_img = None
    bo5_blue_dot = None
    bo5_yellow_val = 0
    bo5_yellow_img = None
    bo5_yellow_dot = None
    font = None

    def __init__(self, *args, **kwargs):
        return super(HUD, self).__init__(*args, **kwargs)

    def update(self,time,events):
        self.update_score_surface()

    def draw(self,screen):
        screen.blit(self.score_blue_draw,(100,0))
        screen.blit(self.score_yellow_draw,(674,0))
        if self.bo5_visible:
            screen.blit(self.bo5_blue_img,(75,768-self.bo5_blue_img.get_height()-5))
            screen.blit(self.bo5_yellow_img,(731,768-self.bo5_yellow_img.get_height()-5))
            for point in range(1,self.bo5_blue_val+1):
                screen.blit(self.bo5_blue_dot,(75+(point)*3+40*(point-1),768-self.bo5_blue_dot.get_height()-3-5))
            for point in range(1,self.bo5_yellow_val+1):
                screen.blit(self.bo5_yellow_dot,(731+(point)*3+40*(point-1),768-self.bo5_yellow_dot.get_height()-3-5))

    def reset_values(self,reset_score=False,bo5_visible=False):
        if reset_score:
            self.score_blue = 0
            self.score_yellow = 0
        self.bo5_visible = bo5_visible
        self.bo5_blue_val = 0
        self.bo5_yellow_val = 0

    def set_bo5score(self,player,score):
        if not (score > 5 or score < 0):
            if player == 0:
                self.bo5_blue_val = score
            else:
                self.bo5_yellow_val = score

    def get_bo5score(self,player):
        if player == 0:
            return self.bo5_blue_val
        else:
            return self.bo5_yellow_val
    
    def set_score(self,player,score):
        if player == 0:
            self.score_blue = score
            self.score_blue_dirty = True
        else:
            self.score_yellow = score
            self.score_yellow_dirty = True

    def get_score(self, player):
        if player == 0:
            return self.score_blue
        else:
            return self.score_yellow

    def initialize(self):
        self.reset_values(True)
        self.score_blue_img = pygame.image.load(os.path.join("data","res","score_blue.png")).convert_alpha()
        self.score_yellow_img = pygame.image.load(os.path.join("data","res","score_yellow.png")).convert_alpha()
        self.bo5_blue_dot = pygame.image.load(os.path.join("data","res","bo5-dot_blue.png")).convert_alpha()
        self.bo5_yellow_dot = pygame.image.load(os.path.join("data","res","bo5-dot_yellow.png")).convert_alpha()
        self.bo5_blue_img = pygame.image.load(os.path.join("data","res","bo5-board_blue.png")).convert_alpha()
        self.bo5_yellow_img = pygame.image.load(os.path.join("data","res","bo5-board_yellow.png")).convert_alpha()
        self.font = pygame.font.Font(pygame.font.get_default_font(),45)
        self.score_blue_draw = pygame.Surface((self.score_blue_img.get_width(),self.score_blue_img.get_height())).convert_alpha()
        self.score_yellow_draw = pygame.Surface((self.score_yellow_img.get_width(),self.score_yellow_img.get_height())).convert_alpha()
        self.update_score_surface()

    def update_score_surface(self):
        if self.score_blue_dirty:
            self.score_blue_draw.blit(self.score_blue_img,(0,0))
            size = self.font.size(str(self.score_blue))
            text = self.font.render(str(self.score_blue),True,(0,0,0))
            self.score_blue_draw.blit(text,(226-size[0],0))
            self.score_blue_dirty = False
        if self.score_yellow_dirty:
            self.score_yellow_draw.blit(self.score_yellow_img,(0,0))
            size = self.font.size(str(self.score_yellow))
            text = self.font.render(str(self.score_yellow),True,(0,0,0))
            self.score_yellow_draw.blit(text,(226-size[0],0))
            self.score_yellow_dirty = False


