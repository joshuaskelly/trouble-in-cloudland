import pygame
import utility
import actor
import vector
import animation

from actor import *

class Icon(actor.Actor):
    def __init__(self, imageFile):
        actor.Actor.__init__(self)
        
        self.animationList = animation.Animation()
        self.animationList.buildAnimation("Idle", [imageFile])
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.position = vector.vector2d(26,68)
        self.velocity = vector.vector2d.zero
        
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    