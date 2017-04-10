import utility
import pygame
import actor
import vector
import random
import animation
import copy
import settings

from actor import *
from settings import *

def loadData():
    smokeParticle.MasterAnimationList.buildAnimation("Idle", ["ppuff"])
    starParticle.MasterAnimationList.buildAnimation("Idle", ["pstaar0","pstaar1","pstaar2"])
    heartParticle.MasterAnimationList.buildAnimation("Idle", ["pheart"])
    rainParticle.MasterAnimationList.buildAnimation("Idle", ["prain"])


    
class smokeParticle(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, velocity):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.canCollide = False
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d(velocity)
        
        self.lifeTimer = int(.5 * FRAMES_PER_SECOND)
        
        self.speed = 3
        
        self.velocity.setMagnitude(self.speed)

    def actor_update(self):
        if self.lifeTimer == 0:
            self.die()
            
        self.lifeTimer -= 1
        self.velocity += [0.0,-.75]

class starParticle(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.canCollide = False
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        
        self.lifeTimer = int(.15 * FRAMES_PER_SECOND)
        
        self.speed = 1
        self.velocity.setMagnitude(self.speed)
        
    def actor_update(self):
        if self.lifeTimer == 0:
            self.die()
            
        self.lifeTimer -= 1

class heartParticle(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        actor.Actor.__init__(self)
        
        self.name = "Heart Particle"
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.canCollide = False
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        
        self.lifeTimer = int(.5 * FRAMES_PER_SECOND)
        
        
        
    def actor_update(self):
        if self.lifeTimer == 0:
            self.die()
            
        self.lifeTimer -= 1
        
        
        
        
class rainParticle(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        
        self.canCollide = False
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [0,-512,SCREEN_WIDTH,SCREEN_HEIGHT]
        
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.up
        
        self.lifeTimer = -1
        
        
        
    def actor_update(self):
        if self.lifeTimer == 0:
            self.die()
            
        self.lifeTimer -= 1
        self.velocity += [0.0,2.0]
        
        
        
class particleEmitter:
    def __init__(self, position, positionJitter, effectsGroup, particleData, emissionAngle, emissionAngleJitter, emissionSpeed, emissionSpeedJitter, emissionRate, emissionCount, lifeTimer = -1):
        self.lifeTimer = lifeTimer
        
        self.ParticleData = particleData
        
        self.emissionAngle = emissionAngle
        self.emissionAngleJitter = emissionAngleJitter
        self.emissionSpeed = emissionSpeed
        self.emissionSpeedJitter = emissionSpeedJitter
        self.emissionRate = emissionRate
        self.emissionCount = emissionCount
        self.offset = vector.Vector2d.zero
        
        self.emissionVector = vector.Vector2d.up
        
        self.position = position
        self.positionJitter = positionJitter
        
        self.mount = None
        
        self.effectsGroup = effectsGroup
    
    
    
    def update(self):
        try:
            if settings_list[PARTICLES]:
                if self.lifeTimer:
                    if self.mount:
                        self.position = self.mount.position + self.offset
                        
                    if not self.lifeTimer % self.emissionRate:
                        for particle in self.ParticleData:
                            particleCount = self.emissionCount
                            while particleCount:
                                self.createParticle(particle)
                                particleCount -= 1
                            
                    self.lifeTimer -= 1
                
                if not self.lifeTimer:
                    self = None
        except:
            pass
        
    def createParticle(self, particle):
        self.emissionVector.setMagnitude(self.emissionSpeed + (random.random() * 2 * self.emissionSpeedJitter) - (self.emissionSpeedJitter) )
        self.emissionVector.setAngle(self.emissionAngle + (random.random() * 2 * self.emissionAngleJitter) - (self.emissionAngleJitter) )
        
        if particle == "heart":
            tempParticle = heartParticle()
            
        if particle == "star":
            tempParticle = starParticle()
            
        if particle == "puff":
            tempParticle = smokeParticle([0,0],[0,0])
            
        if particle == "rain":
            tempParticle = rainParticle()

        tempParticle.position = self.position + (((random.random() * 2.0)-1.0) * self.positionJitter)
        tempParticle.velocity = self.emissionVector.copy()
        
        self.effectsGroup.add(tempParticle)
    
    
    def mountTo(self, object, offset = vector.Vector2d.zero):
        self.mount = object
        self.offset = offset
        
class deathEmitter:
    def __init__(self, position, particleGroup):
        self.particleGroup = particleGroup
        self.position = vector.Vector2d(position)
    
    
    
    def run(self):
        if settings_list[PARTICLES]:
            particlesToCreate = 4
            while particlesToCreate:
                tempVelocity = vector.Vector2d.right
                tempVelocity.setAngle(random.random() * 360)
                tempVelocity.setMagnitude(5.0)
                
                tempParticle = smokeParticle(self.position,tempVelocity)
                
                self.particleGroup.add(tempParticle)
                
                particlesToCreate -= 1