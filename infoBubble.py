import pygame
import settings
import actor
import vector
import utility

from settings import *
from actor import *


class infoBubble(actor.Actor):
    def __init__(self, surface, target, lifeTimer = -1):
        actor.Actor.__init__(self)
        
        self.surface = surface
        self.surfaceRect = self.surface.get_rect()
        self.mounted = False
        self.target = target
        self.image = None
        self.balloonPointerDown = utility.loadImage("balloonPointerDown")
        self.balloonPointerUp = utility.loadImage("balloonPointerUp")
        self.balloonPointerDirection = "Down"
        self.rect = None
        self.velocity = vector.Vector2d.zero
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        self.bound_style = BOUND_STYLE_CUSTOM
        self.offset = vector.Vector2d.zero
        
        self.lifeTimer = lifeTimer
        
        try:
            self.position = target.position + self.offset
            self.mounted = True
        except:#This would cause an error, position isn't defined any where
            self.position = position + self.offset
        
        self.createBubble()
        self.update()
    
    def actor_update(self):
        if self.lifeTimer:
            if self.mounted:
                self.position = self.target.position + self.offset + vector.Vector2d(self.target.hitrect_offset_x, self.target.hitrect_offset_y)
            
            self.lifeTimer -= 1
            
        if not self.lifeTimer:
            self.die()
            
        

    def setOffSet(self,offSet):
        self.offset = offSet
        self.position += self.offset

    def createBubble(self):
        whiteBox = pygame.Surface((self.surface.get_width() + 6, self.surface.get_height() + 6))
        whiteBox.fill((255,255,255))
        whiteBoxRect = whiteBox.get_rect()
        darkBox = pygame.Surface((self.surface.get_width() + 14, self.surface.get_height() + 14))
        darkBox.fill(FONT_COLOR)
        darkBoxRect = darkBox.get_rect()
        
        self.balloonPointerRect = self.balloonPointerDown.get_rect()
        
        self.image = pygame.Surface((darkBox.get_width(), darkBox.get_height() + 38))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
        darkBoxRect.center = self.rect.center
        whiteBoxRect.center = darkBoxRect.center
        self.surfaceRect.center = whiteBoxRect.center
        self.balloonPointerRect.center = whiteBoxRect.center
        
        self.image.blit(darkBox,darkBoxRect)
        self.image.blit(whiteBox,whiteBoxRect)
        self.image.blit(self.surface,self.surfaceRect)
        
        if self.offset.y <= 0 and self.balloonPointerDirection == "Down":
            self.balloonPointerRect.top = whiteBoxRect.bottom
            self.image.blit(self.balloonPointerDown,self.balloonPointerRect)
            self.balloonPointerDirection = "Up"

        if self.offset.y > 0 and self.balloonPointerDirection == "Up":
            self.balloonPointerRect.bottom = whiteBoxRect.top
            self.image.blit(self.balloonPointerUp,self.balloonPointerRect)
            self.balloonPointerDirection = "Down"
        
        self.bounds = [self.image.get_width() / 2,self.image.get_height() / 2 ,SCREEN_WIDTH - (self.image.get_width() / 2),SCREEN_HEIGHT - (self.image.get_height() / 2)]
        
        
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
    def custom_bounds(self):
        if self.position.y < self.bounds[TOP] or self.position.y > self.bounds[BOTTOM]:
            self.offset *= -1
            self.createBubble()
            
        if self.position.x < self.bounds[LEFT]:
            self.position = vector.Vector2d(self.bounds[LEFT], self.position.y)
        elif self.position.x > self.bounds[RIGHT]:
            self.position = vector.Vector2d(self.bounds[RIGHT], self.position.y)