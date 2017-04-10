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
import vector

from settings import *

def loadData():
    Moono.deathSound = utility.loadSound("pop")
    Moono.MasterAnimationList.buildAnimation("Idle", ["moono"])

class Moono(enemy.Enemy):
    deathSound = None
    MasterAnimationList = animation.Animation()
    def __init__(self, targetObject, groupList):

        """   COMMON VARIABLES   """
        enemy.Enemy.__init__(self)
        self.actorType = ACTOR_TYPE_ENEMY   
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [-32,-32,(SCREEN_WIDTH + 32),(SCREEN_HEIGHT + 32)]        
        
        self.canCollide = True        
        self.hitrect = pygame.Rect(0,0,54,98)

        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        """   UNIQUE VARIABLES   """
        self.speed = 3
        self.target = targetObject
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.health = 2

        self.bossFight = False
        self.dropItem = False
        self.dropBalloon = False
        self.dropReflect = False

        aitools.spawnAwayFromTarget(self, self.target)



    def actor_update(self):
        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.processAI()



    def processAI(self):
        aitools.goToTarget(self, self.target)


    
    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
    
    
    
    def die(self):
        utility.play_sound(self.deathSound)

        particle.deathEmitter(self.position, self.effectsGroup).run()

        if self.dropBalloon:
            self.powerupGroup.add(balloon.Bonus250(self.position, self.textGroup))
        elif self.dropReflect:
            self.powerupGroup.add(gem.Reflect(self.position, self.textGroup))
        else:
            self.itemDrop()

        self.kill()
        del self