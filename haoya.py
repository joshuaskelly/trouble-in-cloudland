import utility
import pygame
import random
import balloon
import gem
import text
import aitools
import particle
import actor
import vector
import animation
import copy
import enemy

from settings import *

def loadData():
    Haoya.deathSound = utility.loadSound("pop")
    Haoya.MasterAnimationList.buildAnimation("Idle","haoya")

class Haoya(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, target_object, groupList):
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
       self.hitrect = pygame.Rect(0,0,54,58)
       self.hitrectOffsetY = 6

       self.velocity = vector.vector2d.zero

       """   UNIQUE VARIABLES   """
       self.speed = 2
       self.target = target_object
       self.powerupGroup = groupList[POWERUP_GROUP]
       self.textGroup = groupList[TEXT_GROUP]
       self.effectsGroup = groupList[EFFECTS_GROUP]
       self.health = 3
       self.bossFight = False
       self.dropItem = False
       
       self.deathEmitter = particle.particleEmitter(vector.vector2d.zero,
                        self.effectsGroup,
                        ["puff"],
                        0.0,360.0,
                        5.0,0.0,
                        1.0,4.0,
                        -1.0)
       
       self.deathEmitter.mountTo(self)

       """    LEAVE SCREEN VARIABLES    """
       self.lifeTimer = 10 * FRAMES_PER_SECOND
       self.leaveScreen = False

       aitools.spawnOffScreen(self)



    def processAI(self):
        if self.leaveScreen:
            pass
        elif self.active:
            """Find the distance to the player"""

            magnitude = self.target.position - self.position
            if magnitude.getMagnitude() < 250:
                """If the player is within x distance then
                charge the player."""
                self.speed = 7
            else:
                self.speed = 2

            aitools.goToTarget(self, self.target)



    def actorUpdate(self):
        self.lifeTimer -= 1
        
        if not self.lifeTimer:
            self.leaveScreen = True
            self.speed = 7
            aitools.goToPoint(self,aitools.pointOffScreen())

        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.processAI()



    def customBounds(self):
        if self.leaveScreen:
            self.kill()

    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.hurt(1)