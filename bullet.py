import utility
import pygame
import actor
import vector
import particle
import random
import copy

from actor import *
from settings import *

def loadData():
    Bullet.MasterAnimationList.buildAnimation("Idle",["staar0","staar1","staar2","staar3","staar4","staar5"])
    Bullet.MasterAnimationList.buildAnimation("Reflect",["staar10","staar11","staar12","staar13","staar14","staar15"])
    Bullet.MasterAnimationList.buildAnimation("Damage",["staar20","staar21","staar22","staar23","staar24","staar25"])
    Bullet.MasterAnimationList.buildAnimation("DamageReflect",["staar20","staar21","staar22","staar13","staar14","staar15"])
    Bullet.MasterAnimationList.buildAnimation("Nova",["staar30","staar31","staar32","staar33","staar34","staar35"])

class Bullet(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, velocity, effectsGroup,
                 damage = 1,
                 defaultBoundStyle = BOUND_STYLE_KILL,
                 defaultCollideStyle = COLLIDE_STYLE_HURT):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_BULLET        
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()

        if defaultCollideStyle == COLLIDE_STYLE_NOVA:
            self.boundStyle = BOUND_STYLE_NONE
        else:
            self.boundStyle = defaultBoundStyle

        self.bounds = [-32,-32,SCREEN_WIDTH + 32,SCREEN_HEIGHT + 32]
                
        self.canCollide = False
        self.hitrect = self.rect
        
        self.position = vector.vector2d(position)
        self.velocity = vector.vector2d(velocity)
        
        self.effectsGroup = effectsGroup
        
        self.owner = self

        """   UNIQUE VARIABLES   """
        self.collideStyle = defaultCollideStyle
        self.damage = damage
        self.lifeTimer = 2 * FRAMES_PER_SECOND
        
        self.sequenceList = [[0,1,2,3,4,5],[0]]


    def actorUpdate(self):
        if self.collideStyle == COLLIDE_STYLE_NOVA:
            self.velocity += self.velocity.getPerpendicular().makeNormal() * 5
        
        if not self.lifeTimer % 3 and settingList[PARTICLES]:
            tempParticle = particle.starParticle()
            tempParticle.position = self.position.copy()
            
            self.effectsGroup.add(tempParticle)
        
        self.active = True
        self.lifeTimer -=  1
        
        if self.lifeTimer == 0:
            self.die()


        
    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_TYPE_BOSS:
            self.objectCollidedWith.bulletCollide(self)

        elif self.collideStyle == COLLIDE_STYLE_HURT:
            if self.objectCollidedWith.actorType == ACTOR_TYPE_ENEMY:
                self.objectCollidedWith.health -= self.damage

            self.die()
         
        elif self.collideStyle == COLLIDE_STYLE_REFLECT:
            if self.objectCollidedWith.actorType == ACTOR_TYPE_BAAKE:
                if self.position.x < self.objectCollidedWith.position.x - 64:
                    self.position = vector.vector2d(self.objectCollidedWith.position.x - 104,self.position.y)
                    self.velocity *= [-1.0, 1.0]
                elif self.position.x > self.objectCollidedWith.position.x + 64:
                    self.position = vector.vector2d(self.objectCollidedWith.position.x + 104,self.position.y)
                    self.velocity *= [-1.0, 1.0]
                if self.position.y < self.objectCollidedWith.position.y - 32:
                    self.position = vector.vector2d(self.position.x, self.objectCollidedWith.position.y - 104)
                    self.velocity *= [1.0, -1.0]
                elif self.position.y > self.objectCollidedWith.position.y + 32:
                    self.position = vector.vector2d(self.position.x, self.objectCollidedWith.position.y + 104)
                    self.velocity *= [1.0, -1.0]
            else:
                    self.objectCollidedWith.health -= self.damage

                    self.die()

        elif self.collideStyle == COLLIDE_STYLE_NOVA:
            if self.objectCollidedWith.actorType == ACTOR_TYPE_ENEMY:
                self.objectCollidedWith.health = 0
        
        elif self.collideStyle == COLLIDE_STYLE_NONE:
            pass
        
    def die(self):
        if self.objectCollidedWith.actorType == ACTOR_TYPE_BAAKE:
            if settingList[PARTICLES]:
                starsToCreate = 1
            
                while starsToCreate:
                    starsToCreate -= 1
                    tempPuff = particle.smokeParticle(self.position,
                                                             [1,0])
                    tempPuff.velocity.setAngle(359 * random.random())
                    self.effectsGroup.add(tempPuff)
        self.kill()
        
        
    def setOwner(self, newOwner):
        self.owner = newOwner
        
    def setLifeTimer(self, newLife):
        self.lifeTimer = newLife