import utility
import pygame
import actor
import bullet
import math
import menu
import vector
import random
import text
import copy
import particle

import infoBubble

from actor import *

def loadData():
    Player.MasterAnimationList.buildAnimation("Idle", ["kuunIdle"])
    Player.MasterAnimationList.buildAnimation("Fire", ["kuunShoot"])
    Player.MasterAnimationList.buildAnimation("HurtIdle", ["kuunIdle","blank"])
    Player.MasterAnimationList.buildAnimation("HurtFire", ["kuunShoot","blank"])
    Player.MasterAnimationList.buildAnimation("Die", ["kuunDie"])

    Player.NUM_OW_SOUNDS = 2 #plus one for a total of 3
    Player.loseLifeSound.append(utility.loadSound("ow1"))
    Player.loseLifeSound.append(utility.loadSound("ow2"))
    Player.loseLifeSound.append(utility.loadSound("ow3"))

    Player.NUM_FIRE_SOUNDS = 2 #plus one for total of 3
    Player.fireSound.append(utility.loadSound("shot1"))
    Player.fireSound.append(utility.loadSound("shot2"))
    Player.fireSound.append(utility.loadSound("shot3"))

    Player.deathSound.append(utility.loadSound("playerDeath1"))
    Player.deathSound.append(utility.loadSound("playerDeath2"))
    Player.deathSound.append(utility.loadSound("playerDeath3"))

    Player.extraLifeSound = utility.loadSound("extraLife")

class Player(actor.Actor):
    deathSound = []
    fireSound = []
    loseLifeSound = []
    MasterAnimationList = animation.Animation()
    def __init__(self, bulletGroup, effectsGroup, lifeBoard, scoreBoard):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_PLAYER
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle")
        
        self.rect = self.image.get_rect()
                
        self.boundStyle = BOUND_STYLE_REFLECT
        self.bounds = [0 + 46,0 + 60,SCREEN_WIDTH - 46,SCREEN_HEIGHT - 32]
        
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,80,90)

        self.position = vector.vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        self.velocity = vector.vector2d.zero

        """   UNIQUE VARIABLES   """
        self.bulletSpeed = BULLET_SPEED
        self.defaultFireTimer = 2
        self.resetFireTimer = self.defaultFireTimer
        self.fireTimer = self.resetFireTimer
        self.maxSpeed = 54
        self.hitrectOffsetY = -15
        self.score = 0
        self.lives = 3
        self.stunTimer = 0
        self.lifeBoard = lifeBoard
        self.scoreBoard = scoreBoard
        self.lifeBoard.setText('x' + str(self.lives))
        self.scoreBoard.setText(self.score)
        self.nextBonus = 50000
        
        self.dying = 0
        self.dead = False

        """    BONUS VARIABLES    """
        self.damageBonus = 0
        self.reflectBonus = 0
        self.duelShot = 0
        self.fastShot = 0

        self.pointBonus = 0
        self.comboBonus = 0
        self.comboKills = 0

        """    BULLET VARIABLES   """
        self.bulletDamage = 1
        self.bulletBoundStyle = BOUND_STYLE_KILL
        self.bulletCollideStyle = COLLIDE_STYLE_HURT
        self.bulletGroup = bulletGroup
        self.effectsGroup = effectsGroup

        """    SOUND VARIABLES    """
        self.currentSound = 0


    def actorUpdate(self):
        if self.lives <= 0:
            self.active = False
            self.velocity -= vector.vector2d(0.0,-0.3)
            self.die()
            return
        
        if not self.damageBonus:
            self.bulletDamage = 1
        if not self.reflectBonus:
            self.bulletBoundStyle = BOUND_STYLE_KILL
            self.bulletCollideStyle = COLLIDE_STYLE_HURT
        if not self.fastShot:
            self.resetFireTimer = self.defaultFireTimer

        if self.pointBonus: self.pointBonus -= 1
        if self.damageBonus: self.damageBonus -= 1
        if self.reflectBonus: self.reflectBonus -= 1
        if self.duelShot: self.duelShot -= 1
        if self.stunTimer: self.stunTimer -= 1
        if self.fastShot: self.fastShot -= 1

        if self.comboBonus:
            self.comboBonus -= 1
            if not self.comboBonus:
                comboCounter = 0
                bonusPoints = 0
                while comboCounter <= self.comboKills:
                    comboCounter += 1
                    bonusPoints += comboCounter * 25

                self.incrementScoreNoText(bonusPoints)

                tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Combo Points:" + str(bonusPoints) + "!").image
                
                helpBubble = infoBubble.infoBubble(tempImage, self,1.5 * FRAMES_PER_SECOND)
                helpBubble.offSet = vector.vector2d(0.0, -100.0)
                self.bulletGroup.add(helpBubble)

                self.comboKills = 0

        self.fireTimer -= 1

        self.velocity *= .95
        

        if not self.active:
            self.active = True

        if not self.fireTimer:
            self.animationList.stop("Idle", self.animationList.currentFrame)

        if self.stunTimer:
            self.animationList.play("HurtIdle", self.animationList.currentFrame)
            
    def die(self):
        if self.dying == 0:
            deathType = int(random.random() * 3)
            
            #print deathType
            if deathType == 0:
                tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Blast!").image
                utility.playSound(self.deathSound[0], OW_CHANNEL)
            elif deathType == 1:
                tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh No!").image
                utility.playSound(self.deathSound[1], OW_CHANNEL)
            elif deathType == 2:
                tempImage = text.TextSurface(FONT_PATH, 30,FONT_COLOR, "Bother!").image
                utility.playSound(self.deathSound[2], OW_CHANNEL)
            
            self.animationList.play("Die")
            self.bounds = [-1000, -1000, SCREEN_WIDTH + 1000, SCREEN_HEIGHT + 32]
            self.boundStyle = BOUND_STYLE_CUSTOM
                
            helpBubble = infoBubble.infoBubble(tempImage, self, 5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            self.bulletGroup.add(helpBubble)
        
        self.dying += 1
        
        if settingList[PARTICLES] and not self.dying % 2:
            puffsToCreate = 4
            
            while puffsToCreate:
                puffsToCreate -= 1
                tempPuff = particle.smokeParticle(self.position,
                                                  [1,0])
                tempPuff.velocity.setAngle(359 * random.random())
                self.effectsGroup.add(tempPuff)
                
    def customBounds(self):
        self.dead = True

    def hurt(self, value):
        if self.stunTimer <= 0:
            self.animationList.play("HurtIdle", self.animationList.currentFrame)
            self.lives -= value
            soundToPlay = random.randint(0,2)
            if self.lives != 0:
                utility.playSound(self.loseLifeSound[soundToPlay],OW_CHANNEL)
            self.lifeBoard.setText('x' + str(self.lives))
            self.stunTimer = 1.5 * FRAMES_PER_SECOND            

    def incrementScoreNoText(self,value):
        self.score += value
        self.scoreBoard.setText(self.score)
        
        if self.score > self.nextBonus:
            utility.playSound(self.extraLifeSound, OW_CHANNEL)
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Extra Life!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self,1.5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            self.effectsGroup.add(helpBubble)

            self.lives += 1
            self.lifeBoard.setText('x' + str(self.lives))
            self.nextBonus += 50000

    def incrementScore(self, value, textPosition, textGroup):
        if self.comboBonus and value <= 250:
            self.comboBonus += int(.2 * FRAMES_PER_SECOND)
            self.comboKills += 1
            tempImage = text.Text(FONT_PATH, 30, FONT_COLOR, "x" + str(self.comboKills) + "!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self,0.5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            self.bulletGroup.add(helpBubble)


        if self.pointBonus:
            value *= 2

        tempText = text.Text(FONT_PATH, 36, FONT_COLOR, str(value), 15)
        tempText.setAlign(CENTER_MIDDLE)
        tempText.position = vector.vector2d(textPosition)
        textGroup.add(tempText)

        self.score += value
        self.scoreBoard.setText(self.score)
        
        if self.score >= self.nextBonus:
            utility.playSound(self.extraLifeSound, OW_CHANNEL)
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Extra Life!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self,1.5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            textGroup.add(helpBubble)

            self.lives += 1
            self.lifeBoard.setText('x' + str(self.lives))
            self.nextBonus += 50000

    def fire(self):        
        if self.stunTimer:
            self.animationList.play("HurtFire", self.animationList.currentFrame)
        else:
            self.animationList.play("Fire")

        if (self.fireTimer <= 0):
            utility.playSound(self.fireSound[random.randint(0,2)],PLAYER_CHANNEL)
            if self.velocity:
                bulletVelocity = vector.vector2d(self.velocity)
                bulletVelocity.setMagnitude(self.bulletSpeed)
                
                newBullet = bullet.Bullet((self.position),
                                          (bulletVelocity),
                                          self.effectsGroup,
                                          self.bulletDamage,
                                          self.bulletBoundStyle,
                                          self.bulletCollideStyle)
                newBullet.setOwner(self)
                if self.reflectBonus and self.damageBonus:
                    newBullet.animationList.play("DamageReflect")
                elif self.bulletCollideStyle == COLLIDE_STYLE_REFLECT: newBullet.animationList.play("Reflect")
                elif self.bulletDamage > 1: newBullet.animationList.play("Damage")

                self.bulletGroup.add(newBullet)
                self.fireTimer = self.resetFireTimer

            if self.duelShot:
                if self.velocity:
                    bulletVelocity = vector.vector2d(self.velocity * -1)
                    bulletVelocity.setMagnitude(self.bulletSpeed)
                    
                    newBullet = bullet.Bullet((self.position),
                                              (bulletVelocity),
                                              self.effectsGroup,
                                              self.bulletDamage,
                                              self.bulletBoundStyle,
                                              self.bulletCollideStyle)
                    newBullet.setOwner(self)
                    if self.reflectBonus and self.damageBonus:
                        newBullet.animationList.play("DamageReflect")
                    elif self.bulletCollideStyle == COLLIDE_STYLE_REFLECT: newBullet.animationList.play("Reflect")
                    elif self.bulletDamage > 1: newBullet.animationList.play("Damage")

                    self.bulletGroup.add(newBullet)
    
    
    
    def setVelocity(self, newVelocity):
        self.velocity = newVelocity
        
        if newVelocity.getMagnitude() > self.maxSpeed:
            self.velocity.setMagnitude(self.maxSpeed)