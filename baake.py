import utility
import pygame
import actor
import random
import aitools
import animation
import copy

from actor import *

def loadData():
    Baake.bulletSound = utility.loadSound("baakeHit")
    
    Baake.MasterAnimationList.buildAnimation("Idle", ["baake"])

class Baake(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        
        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_BAAKE        
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_REFLECT
        self.bounds = [32,32,(SCREEN_WIDTH - 32),(SCREEN_HEIGHT - 32)]
                
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,108,88)
        
        self.position = vector.Vector2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(5.0, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = 5.0
        self.changeDirection = 0

        """    BOSS FIGHT        """
        self.leaveScreen = False

        aitools.spawnOnScreen(self)
    
    
    def actor_update(self):
        if not self.leaveScreen:
            self.processAI()
        else:
            self.bound_style = BOUND_STYLE_KILL

        if not self.active:
            self.active = True
        
        
        
    def processAI(self):
        if not self.changeDirection:
            self.changeDirection = 2 * FRAMES_PER_SECOND
            
            aitools.cardinalDirection(self)
                
        self.changeDirection -= 1
    
    
    def collide(self):
        if self.object_collided_with.actorType == ACTOR_BULLET:
            utility.play_sound(Baake.bulletSound, BAAKE_CHANNEL)

        elif self.object_collided_with.actorType == ACTOR_PLAYER:
                if self.object_collided_with.position.x < self.position.x - 64:
                    self.object_collided_with.position = vector.Vector2d((self.position.x - 94),
                                                                         self.object_collided_with.position.y)
                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= [-1.0, 1.0]
                           
                elif self.object_collided_with.position.x > self.position.x + 64:
                    self.object_collided_with.position = vector.Vector2d((self.position.x + 94),
                                                                         self.object_collided_with.position.y)
                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= [-1.0, 1.0]
                        
                if self.object_collided_with.position.y < self.position.y - 32:
                    self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                         self.position.y - 76)
                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= [1.0, -1.0]
                        
                elif self.object_collided_with.position.y > self.position.y + 32:
                    self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                         self.position.y + 108)
                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= [1.0, -1.0]