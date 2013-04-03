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
    Paajo.deathSound = utility.loadSound("pop")
    Paajo.MasterAnimationList.buildAnimation("Idle","paajo")

class Paajo(enemy.Enemy):
    lastSpawn = [0,0]
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, groupList, myPosition):

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
        self.hitrect = pygame.Rect(0,0,68,74)

        self.position = vector.vector2d.zero
        self.velocity = vector.vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 12
        self.changeDirection = 0
        self.target = [0,0]
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = 2
        self.dropItem = False
        self.bossFight = False
        self.myPosition = myPosition

        """    LEAVE SCREEN VARIABLES    """
        self.lifeTimer = 5 * FRAMES_PER_SECOND
        self.leaveScreen = False

        if self.myPosition == 5:
            aitools.spawnOffScreen(self)
            Paajo.lastSpawn = self.position
        else:
            aitools.spawnAtPoint(self, Paajo.lastSpawn)

        if self.myPosition == 1:
            self.leader = self



    def actorUpdate(self):
        self.lifeTimer -= 1

        if not self.lifeTimer:
            self.leaveScreen = True

        if self.active:
            if self.health <= 0:
                self.die()
                self.active = False
        else:
            self.active = True

        self.process_AI()



    def setGroup(self,myFlock):
        self.myFlock = myFlock
        for element in self.myFlock:
            if element.myPosition == 1:
                self.leader = element



    def process_AI(self):
        if self.leaveScreen:
            pass
        elif self.myPosition != 1:
            flockChart = [False,False,False,False,False]
            for member in self.myFlock:
                if member.active:
                    if member.myPosition == self.myPosition and member != self and self.myPosition < 5:
                        member.myPosition += 1

                    flockChart[member.myPosition - 1] = True
                    
                    if member.myPosition == 1:
                        self.leader = member

            positionNumber = 0
            for element in flockChart:
                positionNumber += 1
                if positionNumber < self.myPosition and element == False:
                    self.myPosition = positionNumber
                    if self.myPosition == 1:
                        self.leader = self

    
                self.speed = 14.2
                leaderVelocity = vector.vector2d(self.leader.velocity[0], self.leader.velocity[1])
                leaderPerpendicular = self.leader.velocity.getPerpendicular()
                if self.myPosition % 2:
                    offset = -50
                else:
                    offset = 50
                targetPoint = self.leader.position - (leaderVelocity.makeNormal() * (100) * int(self.myPosition / 2)) + (leaderPerpendicular.makeNormal() * offset * int(self.myPosition / 2))

                if (targetPoint - self.position).getMagnitude() < self.speed:
                    aitools.goToPoint(self,targetPoint)
                else:
                    aitools.arcToPoint(self, targetPoint, 3)
    
        else:
            for element in self.myFlock:
                if element != self and element.myPosition == self.myPosition:
                    element.myPosition += 1

            self.speed = 11
            if not self.changeDirection:
                self.target = vector.vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                self.changeDirection = 30
            self.changeDirection -= 1
            aitools.arcToPoint(self, self.target)
    
    
    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.hurt(1)
    


    def customBounds(self):
        if self.leaveScreen:
            self.kill()