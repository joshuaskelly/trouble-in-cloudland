import utility
import pygame
import random
import balloon
import gem
import text
import aitools
import particle
import animation
import enemy
import copy
import vector

from settings import *

def loadData():
    Rokubi.deathSound = utility.loadSound("pop")
    Rokubi.MasterAnimationList.buildAnimation("Idle","rokubei")

class Rokubi(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, targetObject, groupList):
        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)

        """    Rokubi Spawning    """
        self.noSpawn = False
        
        self.actorType = ACTOR_TYPE_ENEMY
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")      
        
        self.rect = self.image.get_rect()
        
        self.boundStyle = BOUND_STYLE_NONE
        self.bounds = [-32,-32,(SCREEN_WIDTH + 32),(SCREEN_HEIGHT + 32)]        
        
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,54,98)

        self.velocity = vector.vector2d(0,0)

        """   UNIQUE VARIABLES   """
        self.speed = 7
        self.hideBehind = targetObject
        self.target = targetObject
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.bossGroup = groupList[BOSS_GROUP]
        self.health = 1
        self.dropItem = False
        self.bossFight = False
        self.charging = False
        self.hiding = False

        self.emitter = particle.particleEmitter(vector.vector2d.zero,vector.vector2d.zero,
                                        self.effectsGroup,
                                        ["heart"],
                                        270.0,45.0,
                                        0.0,0.0,
                                        8.0,1.0,
                                        -1.0)
        

        
        self.emitter.mountTo(self)

        aitools.spawnOffScreen(self)
        


    def actorUpdate(self):
        self.emitter.update()
        
        if self.active and self.health <= 0:
            self.health = 0
            self.active = False
            self.die()
        else:
            """This can occasionally cause an error
            if the rokubi has been removed from the
            group by an outside function, such as when
            moving on to a new level."""
            if (not self.bossFight or not self.active and not self.charging) and not self.hiding:
                try:
                    self.hideBehind = aitools.getClosest(self, [self.enemyGroup,self.bossGroup], [ACTOR_TYPE_BAAKE, ACTOR_TYPE_BOSS])
                    if self.hideBehind == self:
                        self.hideBehind = self.target
                except:
                    self.hideBehind = self.target

            self.active = True
            
        self.processAI()



    def processAI(self):
        self.charging = False
        """Find the distance to the player"""

        distance = (self.target.position - self.position).getMagnitude()

        if self.hideBehind.actorType == ACTOR_TYPE_BOSS:
            if distance < 450:
                self.speed = 10
                aitools.goToTarget(self, self.target)
                self.charging = True
                self.hiding = False

        else:
            if distance < 325:
                self.speed = 10
                aitools.goToTarget(self, self.target)
                self.charging = True
                self.hiding = False

        if not self.charging:
            self.speed = 7
            self.hiding = True
            aitools.hide(self, self.hideBehind, self.target)


    
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.hurt(1)