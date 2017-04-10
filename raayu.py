import utility
import pygame
import random
import balloon
import gem
import text
import aitools
import particle
import animation
import copy
import enemy

from settings import *
from actor import *

def loadData():
    Raayu.deathSound = utility.loadSound("pop")
    Raayu.MasterAnimationList.buildAnimation("Idle", ["raayu"])

class Raayu(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, target_object, groupList):

        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        self.actorType = ACTOR_TYPE_ENEMY    
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-32,-32,(SCREEN_WIDTH + 32),(SCREEN_HEIGHT + 32)]        
        
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,66,82)

        """   UNIQUE VARIABLES   """
        self.speed = 9
        self.target = target_object
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = 2
        self.dropItem = False
        self.bossFight = False

        """    LEAVE SCREEN VARIABLES    """
        self.lifeTimer = 5 * FRAMES_PER_SECOND
        self.leaveScreen = False

        done = aitools.spawnOffScreen(self)



    def actor_update(self):
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
        aitools.arcToPoint(self,self.target.position,2)

    
    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
    


    def custom_bounds(self):
        if self.leaveScreen:
            self.kill()