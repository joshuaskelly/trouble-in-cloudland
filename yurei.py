import utility
import pygame
import random
import math
import balloon
import text
import aitools
import particle
import animation
import copy
import enemy

from actor import *

def loadData():
    Yurei.MasterAnimationList.buildAnimation("Idle", ["yurei"])

class Yurei(enemy.Enemy):
    MasterAnimationList = animation.Animation()
    def __init__(self, groupList):
        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
    
        self.rect = self.image.get_rect()

        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [32,32,(SCREEN_WIDTH - 32),(SCREEN_HEIGHT - 32)]
        self.active = True
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,54,98)

        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 4
        self.target = self
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = -1
        self.changeDirection = 0
        self.targetPoint = vector.Vector2d.zero

        """    LEAVE SCREEN VARIABLES    """
        self.leaveScreen = False

        aitools.spawnOffScreen(self)



    def actor_update(self):
        self.health = -1
        if not self.active:
            self.active = True

        self.processAI()



    def processAI(self):
        if self.leaveScreen:
            pass
        else:
            self.target = aitools.getClosest(self, self.powerupGroup)
    
            if self.target != self and self.target.active:
                aitools.goToTarget(self, self.target)
                self.changeDirection = 0
    
            else:
                if not self.changeDirection:
                    self.targetPoint = vector.Vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                    self.changeDirection = 30
                self.changeDirection -= 1
                
                aitools.arcToPoint(self, self.targetPoint)
    
    
    
    def collide(self):
        if self.object_collided_with.actorType == ACTOR_TYPE_PICKUP:
            self.object_collided_with.die()
    


    def custom_bounds(self):
        if self.leaveScreen:
            self.kill()
    
    def die(self):
        self.kill()
        self = None