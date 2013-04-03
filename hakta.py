import utility
import pygame
import random
import balloon
import gem
import text
import aitools
import particle
import copy
import enemy
import animation
import vector

from settings import *

def loadData():
    Hakta.deathSound = utility.loadSound("pop")
    Hakta.MasterAnimationList.buildAnimation("Idle","hakta")

class Hakta(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, targetObject, groupList):

        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        self.actorType = ACTOR_TYPE_ENEMY       
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.boundStyle = BOUND_STYLE_CUSTOM
        self.bounds = [32,32,(SCREEN_WIDTH - 32),(SCREEN_HEIGHT - 32)]        
        
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,106,104)

        self.position = vector.vector2d.zero
        self.velocity = vector.vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 4
        self.target = targetObject
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = 2
        self.bossFight = False
        self.dropItem = False
        
        """    LEAVE SCREEN VARIABLES    """
        self.lifeTimer = 5 * FRAMES_PER_SECOND
        self.leaveScreen = False

        done = aitools.spawnOffScreen(self)



    def actorUpdate(self):
        self.lifeTimer -= 1
        if not self.lifeTimer:
            self.leaveScreen = True

        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.processAI()



    def processAI(self):
        if self.leaveScreen:
            if self.speed > 5:
                self. speed -= .015
        elif self.speed <= 5:
            self.speed = 13
            aitools.goToTarget(self, self.target)
        else:
            self.speed -= 0.15
            self.velocity = self.velocity.makeNormal() * self.speed



    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.hurt(1)
    


    def customBounds(self):
        if self.leaveScreen:
            self.kill()