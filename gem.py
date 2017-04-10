import animation
import utility
import pygame
import actor
import text
import vector
import copy
import bullet
import infoBubble

from actor import *

def loadData():
    DamageX2.pickupSound = utility.loadSound("doubleDamage")
    DamageX2.MasterAnimationList.buildAnimation("Idle", ["geemred"])
    DamageX2.MasterAnimationList.buildAnimation("Blink", ["geemred","blank"])
    
    Nova.pickupSound = utility.loadSound("nova")
    Nova.MasterAnimationList.buildAnimation("Idle", ["boom"])
    Nova.MasterAnimationList.buildAnimation("Blink", ["boom","blank"])

    Reflect.pickupSound = utility.loadSound("reflect")
    Reflect.MasterAnimationList.buildAnimation("Idle", ["geemblue"])
    Reflect.MasterAnimationList.buildAnimation("Blink", ["geemblue","blank"])

    DualShot.pickupSound = utility.loadSound("dualShot")
    DualShot.MasterAnimationList.buildAnimation("Idle", ["geemgreen"])
    DualShot.MasterAnimationList.buildAnimation("Blink", ["geemgreen","blank"])

    FastShot.pickupSound = utility.loadSound("fastShot")
    FastShot.MasterAnimationList.buildAnimation("Idle", ["geemorange"])
    FastShot.MasterAnimationList.buildAnimation("Blink",["geemorange","blank"])

class Gem(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_PICKUP
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-16,-16,SCREEN_WIDTH + 16, SCREEN_HEIGHT + 16]
        self.bonusTime = 0
        self.lifeTimer = 5 * FRAMES_PER_SECOND

    def actor_update(self):
        if not self.active:
            self.active = True
            
        if not self.lifeTimer:
            self.die()
            
        self.lifeTimer -= 1
            
        if self.lifeTimer < 2 * FRAMES_PER_SECOND:
            self.animation_list.play("Blink")

    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            utility.play_sound(self.pickupSound, PICKUP_CHANNEL)
            self.displayText()
            self.giveBonus()
            self.die()

    def custom_bounds(self):
        if self.position.x < 20.0:
            self.position = vector.Vector2d(20.0, self.position.y)
        if self.position.y < 20.0:
            self.position = vector.Vector2d(self.position.x, 20.0)
        if self.position.x > SCREEN_WIDTH - 20.0:
            self.position = vector.Vector2d(SCREEN_WIDTH - 20.0, self.position.y)
        if self.position.y > SCREEN_HEIGHT - 20.0:
            self.position = vector.Vector2d(self.position.x, SCREEN_HEIGHT - 20.0)

    def die(self):
        self.active = False
        self.kill()
        self = None

class DamageX2(Gem):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):
        Gem.__init__(self)
        """   COMMON VARIABLES   """
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()  
        
        self.hitrect = self.rect
        
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.textGroup = textGroup
        
        
    def displayText(self):
        tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Double Damage!").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.textGroup.add(helpBubble)

    def giveBonus(self):
        self.object_collided_with.damageBonus += 4 * FRAMES_PER_SECOND
        self.object_collided_with.bulletDamage = 2

class Nova(Gem):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup, effectsGroup):

        """   COMMON VARIABLES   """
        Gem.__init__(self)
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect()
        self.hitrect = self.rect

        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.textGroup = textGroup
        self.effectsGroup = effectsGroup
        
        
    def displayText(self):
        tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Nova!").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.textGroup.add(helpBubble)



    def giveBonus(self):
        starsToCreate = 15

        while starsToCreate:
            starsToCreate -= 1
            tempBullet = bullet.Bullet((self.position), 
                                        (BULLET_SPEED,0),
                                         self.effectsGroup,
                                         0,
                                         BOUND_STYLE_KILL, 
                                         COLLIDE_STYLE_NOVA)
            tempBullet.setLifeTimer(13)
            tempBullet.animation_list.play("Nova")
            tempBullet.velocity.setAngle(starsToCreate * 24)
            """bullet damage doesn't matter
            since these bullets automatically
            kill whatever they touch"""

            tempBullet.setOwner(self.object_collided_with)
            self.object_collided_with.bulletGroup.add(tempBullet)

class Reflect(Gem):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):

        """   COMMON VARIABLES   """
        Gem.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.textGroup = textGroup



    def displayText(self):
        tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Reflect!").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.textGroup.add(helpBubble)



    def giveBonus(self):
        self.object_collided_with.bulletbound_style = BOUND_STYLE_REFLECT
        self.object_collided_with.bulletCollideStyle = COLLIDE_STYLE_REFLECT
        self.object_collided_with.reflectBonus += 2.5 * FRAMES_PER_SECOND

class DualShot(Gem):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):

        """   COMMON VARIABLES   """
        Gem.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.textGroup = textGroup



    def displayText(self):
        tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Dual Shot!").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.textGroup.add(helpBubble)



    def giveBonus(self):
        self.object_collided_with.duelShot += 3 * FRAMES_PER_SECOND

class FastShot(Gem):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):

        """   COMMON VARIABLES   """
        Gem.__init__(self)
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("Idle")
        
        self.rect = self.image.get_rect() 
        self.hitrect = self.rect
        
        self.position = vector.Vector2d(position)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.textGroup = textGroup

    def displayText(self):
        tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Fast Shot!").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.object_collided_with, 1.5 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.textGroup.add(helpBubble)

    def giveBonus(self):
        self.object_collided_with.fastShot += 3 * FRAMES_PER_SECOND
        self.object_collided_with.resetFireTimer = 1
