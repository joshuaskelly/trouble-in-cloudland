import utility
import pygame
import random
import math
import balloon
import gem
import text
import aitools
import particle
import animation
import copy
import enemy

from actor import *

def loadData():
    Batto.lastSpawn = [0,0]
    Batto.deathSound = utility.loadSound("pop")
    Batto.MasterAnimationList.buildAnimation("Idle","batto")

class Batto(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, groupList, leader = None):

        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        self.actorType = ACTOR_TYPE_ENEMY
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.boundStyle = BOUND_STYLE_CUSTOM    
        self.bounds = [-32,-32,(SCREEN_WIDTH + 32),(SCREEN_HEIGHT + 32)]        
        
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,80,66)

        self.position = vector.vector2d.zero
        self.velocity = vector.vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 10
        self.changeDirection = 0
        self.target = [0,0]
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = 1
        self.bossFight = False
        self.dropItem = False
        
        """    EXIT GAME VARIABLES    """
        self.onScreen = 0
        self.dead = False

        if leader == None:
            self.leader = self
            aitools.spawnOffScreen(self,128)
            Batto.lastSpawn = self.position
        else:
            self.leader = leader
            aitools.spawnAtPoint(self, Batto.lastSpawn)


    def actorUpdate(self):
        if self.active:
            if self.health <= 0:
                self.die()

            self.onScreen += 1
            self.processAI()

            if self.leader.active == False:
                self.leader = self
        else:
            self.active = True




    def processAI(self):
        if self.leader.dead == True:
            pass
        elif self.leader.active and self.leader != self:
            tempVelocity = vector.vector2d(self.leader.velocity[0], self.leader.velocity[1])
            targetPoint = self.leader.position - (tempVelocity.makeNormal()) * vector.vector2d(150,150)
            aitools.goToPoint(self, targetPoint)
        else:
            if not self.changeDirection:
                self.target = vector.vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                self.changeDirection = 30
            self.changeDirection -= 1
            aitools.arcToPoint(self, self.target)

    

    def customBounds(self):
        if self.onScreen > FRAMES_PER_SECOND:
            self.active = False
            self.dead = True

        self.onScreen = 0
        
        if self.dead:
            self.kill()
            self = None

    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.hurt(1)