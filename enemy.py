import utility
import pygame
import actor
import random
import balloon
import gem
import text
import aitools
import particle
import animation
import copy

from settings import *
from actor import *

class Enemy(actor.Actor):
    deathSound = None
    def __init__(self):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_ENEMY    
        
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = [-32,-32,(SCREEN_WIDTH + 32),(SCREEN_HEIGHT + 32)]        
        
        self.canCollide = True

        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        self.bossFight = False
        self.dropItem = False
        self.dropBalloon = False



    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
    
    
    def itemDrop(self):
        if self.dropItem:
            self.powerupGroup.add(gem.Nova(self.position, self.textGroup, self.effectsGroup))

        elif self.bossFight:
            randomNumber = int(random.random() * 25)
            
            if not randomNumber:
                self.powerupGroup.add(gem.Reflect(self.position, self.textGroup))
            elif randomNumber == 1:
                self.powerupGroup.add(gem.DamageX2(self.position, self.textGroup))
            elif randomNumber == 2:
                self.powerupGroup.add(gem.FastShot(self.position,self.textGroup))
            elif randomNumber == 3:
                self.powerupGroup.add(gem.DualShot(self.position,self.textGroup))

        elif self.object_collided_with.owner.combo_bonus:
            self.object_collided_with.owner.increment_score(100, self.position, self.textGroup)

            randomNumber = int(random.random() * 6 + 1)
    
            if randomNumber == 1:
                """Generate a random number between 1 and 100"""
                randomNumber = int(random.random() * 100 + 1)


                if randomNumber <= 25:
                    self.powerupGroup.add(balloon.Bonus250(self.position,self.textGroup))
                elif randomNumber <= 40:
                    self.powerupGroup.add(balloon.Bonus500(self.position, self.textGroup))
                elif randomNumber <= 50:
                    self.powerupGroup.add(balloon.BonusX2(self.position,self.textGroup))
                elif randomNumber <= 60:
                    self.powerupGroup.add(gem.DualShot(self.position, self.textGroup))
                elif randomNumber <= 70:
                    self.powerupGroup.add(gem.FastShot(self.position,self.textGroup))
                elif randomNumber <= 80:
                    self.powerupGroup.add(gem.DamageX2(self.position, self.textGroup))
                elif randomNumber <= 90:
                    self.powerupGroup.add(gem.Reflect(self.position, self.textGroup))
                else:
                    self.powerupGroup.add(gem.Nova(self.position,self.textGroup,self.effectsGroup))
        else:
            self.object_collided_with.owner.increment_score(100, self.position, self.textGroup)

            randomNumber = int(random.random() * 6 + 1)
    
            if randomNumber == 1:
                """Generate a random number between 1 and 100"""
                randomNumber = int(random.random() * 100 + 1)


                if randomNumber <= 25:
                    self.powerupGroup.add(balloon.Bonus250(self.position,self.textGroup))
                elif randomNumber <= 40:
                    self.powerupGroup.add(balloon.Bonus500(self.position, self.textGroup))
                elif randomNumber <= 45:
                    self.powerupGroup.add(balloon.BonusCombo(self.position,self.textGroup))
                elif randomNumber <= 50:
                    self.powerupGroup.add(balloon.BonusX2(self.position,self.textGroup))
                elif randomNumber <= 60:
                    self.powerupGroup.add(gem.DualShot(self.position, self.textGroup))
                elif randomNumber <= 70:
                    self.powerupGroup.add(gem.FastShot(self.position,self.textGroup))
                elif randomNumber <= 80:
                    self.powerupGroup.add(gem.DamageX2(self.position, self.textGroup))
                elif randomNumber <= 90:
                    self.powerupGroup.add(gem.Reflect(self.position, self.textGroup))
                else:
                    self.powerupGroup.add(gem.Nova(self.position,self.textGroup,self.effectsGroup))

    def die(self):
        utility.play_sound(self.deathSound)

        particle.deathEmitter(self.position, self.effectsGroup).run()

        self.itemDrop()

        self.active = False
        self.emitter = None
        self.deathEmitter = None
        self.kill()
        del self