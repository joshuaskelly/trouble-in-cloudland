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
    Yurei.MasterAnimationList.buildAnimation("Idle","yurei")

class Yurei(enemy.Enemy):
    MasterAnimationList = animation.Animation()
    def __init__(self, groupList):
        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
    
        self.rect = self.image.get_rect()

        self.boundStyle = BOUND_STYLE_CUSTOM
        self.bounds = [32,32,(SCREEN_WIDTH - 32),(SCREEN_HEIGHT - 32)]
        self.active = True
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,54,98)

        self.position = vector.vector2d.zero
        self.velocity = vector.vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 4
        self.target = self
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = -1
        self.changeDirection = 0
        self.targetPoint = vector.vector2d.zero

        """    LEAVE SCREEN VARIABLES    """
        self.leaveScreen = False

        aitools.spawnOffScreen(self)



    def actorUpdate(self):
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
                    self.targetPoint = vector.vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                    self.changeDirection = 30
                self.changeDirection -= 1
                
                aitools.arcToPoint(self, self.targetPoint)
    
    
    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_TYPE_PICKUP:
            self.objectCollidedWith.die()
    


    def customBounds(self):
        if self.leaveScreen:
            self.kill()
    
    def die(self):
        self.kill()
        self = None