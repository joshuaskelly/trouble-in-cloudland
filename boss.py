import utility
import pygame
import actor
import random
import aitools
import particle
import icon
import animation
import copy

import yurei
import infoBubble

from actor import *
from settings import *

def loadData():
    BossTut.music = utility.loadSound("bossMusic")
    BossTut.bulletSound = utility.loadSound("baakeHit")
    BossTut.hurtSound = utility.loadSound("hurtBoss")
    BossTut.howToKill = utility.loadImage("howToBoss1")
    BossTut.MasterAnimationList.buildAnimation("idle", ["boss1"])
    BossTut.MasterAnimationList.buildAnimation("hurt", ["boss1","boss1","boss1_1","boss1_1"])

    BaakeBoss.music = utility.loadSound("bossMusic")
    BaakeBoss.bulletSound = utility.loadSound("baakeHit")
    BaakeBoss.hurtSound = utility.loadSound("hurtBoss")
    BaakeBoss.howToKill = utility.loadImage("howToBoss1")
    BaakeBoss.MasterAnimationList.buildAnimation("idle", ["boss0"])
    BaakeBoss.MasterAnimationList.buildAnimation("hurt", ["boss0","boss0","boss0_1","boss0_1"])
    
    MoonoBoss.music = utility.loadSound("bossMusic")
    MoonoBoss.bulletSound = utility.loadSound("baakeHit")
    MoonoBoss.hurtSound = utility.loadSound("hurtBoss")
    MoonoBoss.shieldBreak = utility.loadSound("shieldBreak")
    MoonoBoss.shieldRestore = utility.loadSound("shieldRestore")
    MoonoBoss.howToKill = utility.loadImage("howToBoss3")
    MoonoBoss.MasterAnimationList.buildAnimation("idle", ["boss2idle_0","boss2idle_1","boss2idle_2","boss2idle_3","boss2idle_4","boss2idle_5","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0","boss2idle_0"])
    MoonoBoss.MasterAnimationList.buildAnimation("vulnerable", ["boss2v"])
    MoonoBoss.MasterAnimationList.buildAnimation("hurt", ["boss2_1"])
    

####################################################
"""    """    """    MOONO BOSS    """    """    """
####################################################
####################################################
"""    """    """    MOONO BOSS    """    """    """
####################################################
class MoonoBoss(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self,world,target,groupList):
        
        """    COMMON VARIABLES    """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_BOSS
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
        
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,162,148)
        
        self.position = vector.Vector2d(SCREEN_WIDTH + 32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(0.0, 0.0)
        
        """    UNIQUE VARIABLES    """
        self.speed = 3
        self.health = (world.level + 1) * 25
        self.lifeTimer = 0

        self.sequenceList = [[0]]
        
        self.stunned = 0

        self.world = world
        self.target = target

        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]

        self.gaveBonus = False

        """    AI VARIABLES    """
        self.charging = False
        self.timeUntilCharge = 0
        self.spinning = False
        self.timeUntilSpin = 0

    def actor_update(self):
        utility.play_music(self.music, True)
        if not self.active and self.health > 0:
            self.active = True

        if self.lifeTimer <= 30 * FRAMES_PER_SECOND and  self.health == (self.world.level + 1) * 25:
            if self.lifeTimer == 30 * FRAMES_PER_SECOND:
                tempImage = self.howToKill
                
                helpBubble = infoBubble.infoBubble(tempImage, self.target,5 * FRAMES_PER_SECOND)
                helpBubble.offset = vector.Vector2d(0.0, -100.0)
                self.textGroup.add(helpBubble)
            self.lifeTimer += 1

        if self.active:
            if self.stunned:
                if self.charging:
                    self.speed -= 0.2
                    if self.speed <= 1.75:
                        self.speed = 1.75
                        self.charging = False
                        self.timeUntilCharge = 10 * FRAMES_PER_SECOND
                
                    self.velocity.makeNormal()
                    self.velocity *= self.speed

                self.stunned -= 1

                self.animation_list.play("vulnerable")
                
                if not self.stunned:
                    utility.play_sound(self.shieldRestore, PICKUP_CHANNEL)
                    self.animation_list.play("idle")
                
            else:
                self.currentSequence = 0
                self.processAI()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gaveBonus:
                self.world.giveBonus()
                self.gaveBonus = True



    def processAI(self):
        if self.charging:
            self.speed -= 0.2

            if self.speed <= 2:
                self.speed = 2
                self.charging = False
                self.bound_style = BOUND_STYLE_CUSTOM
                self.timeUntilCharge = 6 * FRAMES_PER_SECOND
            
            aitools.goToTarget(self,self.target)

        elif self.spinning:
            self.speed += 0.2
            
            if self.speed >= 40:
                self.speed = 15
                self.charging = True
                self.spinning = False
                self.timeUntilSpin = 7 * FRAMES_PER_SECOND
            
            self.velocity += self.velocity.getPerpendicular().makeNormal()
            self.velocity = self.velocity.makeNormal() * self.speed

        elif self.health <= (self.world.level + 1) * 7:
            if not self.timeUntilCharge:
                self.charge()
            elif not self.timeUntilSpin:
                self.spin()
            else:
                aitools.goToTarget(self,self.target)

        elif self.health <= (self.world.level + 1) * 14:
            if not self.timeUntilCharge:
                self.charge()
            else:
                aitools.goToTarget(self,self.target)

        else:
            aitools.goToTarget(self,self.target)



    def charge(self):
        self.charging = True
        self.speed = 11

        aitools.goToTarget(self,self.target)
        self.bound_style = BOUND_STYLE_REFLECT



    def spin(self):
        self.spinning = True
        self.bound_style = BOUND_STYLE_REFLECT



    def hurt(self,damage):
        self.health -= damage
        self.animation_list.play("hurt")
        utility.play_sound(self.hurtSound, BOSS_CHANNEL)

        if self.health <= 0:
            for actor in self.enemyGroup:
                actor.leaveScreen = True


    def die(self):
        self.velocity[1] += .1
        if self.bound_style == BOUND_STYLE_REFLECT:
            self.bound_style = BOUND_STYLE_CUSTOM

        self.stunned -= 1
        self.world.pauseSpawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffsToCreate = 4
            
            while puffsToCreate and settings_list[PARTICLES]:
                puffsToCreate -= 1
                tempPuff = particle.smokeParticle(self.position,
                                                         [1,0])
                tempPuff.velocity.setAngle(359 * random.random())
                self.effectsGroup.add(tempPuff)



    def bulletCollide(self, bullet):
        if not self.stunned:
            utility.play_sound(self.bulletSound, BAAKE_CHANNEL)
            if bullet.collideStyle == COLLIDE_STYLE_HURT:
                bullet.die()
            
            elif bullet.collideStyle == COLLIDE_STYLE_REFLECT:
                if bullet.position.x < self.position.x - 64:
                    bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                    bullet.velocity *= [-1.0, 1.0]
                elif bullet.position.x > self.position.x + 64:
                    bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                    bullet.velocity *= [-1.0, 1.0]
                if bullet.position.y < self.position.y - 64:
                    bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                    bullet.velocity *= [1.0, -1.0]
                elif bullet.position.y > self.position.y + 64:
                    bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                    bullet.velocity *= [1.0, -1.0]
    
            elif bullet.collideStyle == COLLIDE_STYLE_NOVA:
                utility.play_sound(self.shieldBreak, BAAKE_CHANNEL)
                self.stunned = 2 * FRAMES_PER_SECOND
                self.animation_list.play("vulnerable")
                
                starsToCreate = 15
                
                while starsToCreate:
                    starsToCreate -= 1
                    tempBullet = particle.starParticle()
                    tempVector = vector.Vector2d(120, 0)
                    tempVector.setAngle(starsToCreate * 24)
                    tempBullet.position = vector.Vector2d(self.position + tempVector)
                    tempBullet.lifeTimer = .5 * FRAMES_PER_SECOND
                    tempBullet.velocity = vector.Vector2d(3.0, 0.0)
                    tempBullet.velocity.setAngle(starsToCreate * 24)
                    
                    
                    self.effectsGroup.add(tempBullet)
        
        elif bullet.collideStyle != COLLIDE_STYLE_NOVA:
                bullet.die()
                self.hurt(1)



    def custom_bounds(self):
        if self.health <= 0:
            self.kill()
            self = None


    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER and not self.stunned:
            
            self.object_collided_with.hurt(1)

####################################################
"""    """    """    BAAKE BOSS    """    """    """
####################################################
####################################################
"""    """    """    BAAKE BOSS    """    """    """
####################################################
class BaakeBoss(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self, world, target, groupList):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_BOSS
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = [-64,-64,SCREEN_WIDTH + 64,SCREEN_HEIGHT + 64]
                
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,140,210)
        
        self.position = vector.Vector2d(-32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(0.0, 0.0)
        
        """   UNIQUE VARIABLES   """
        self.speed = 1.75
        self.health = world.level + 2
        self.lifeTimer = 0

        self.sequenceList = [[0],[0,0,1,1]]

        self.stunned = 0

        self.world = world
        self.target = target

        self.groupList = groupList
        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]

        self.eye = icon.Icon("boss0_eye")
        self.textGroup.add(self.eye)

        self.gaveBonus = False

        """    AI VARIABLES    """
        self.charging = False
        self.timeUntilCharge = 0
        
        """    Additional Challenges    """
        self.summonedYurei = False



    def actor_update(self):
        utility.play_music(self.music, True)
        self.placeEye()

        if self.lifeTimer <= 30 * FRAMES_PER_SECOND and self.health == self.world.level+ 2:
            if self.lifeTimer == 30 * FRAMES_PER_SECOND:
                tempImage = self.howToKill
                
                helpBubble = infoBubble.infoBubble(tempImage, self.target,5 * FRAMES_PER_SECOND)
                helpBubble.offset = vector.Vector2d(0.0, -100.0)
                self.textGroup.add(helpBubble)
            self.lifeTimer += 1
            
        if not self.active and self.health > 0:
            self.active = True

        if self.active:
            if self.stunned:
                if self.charging:
                    self.speed -= 0.2
                    if self.speed <= 1.75:
                        self.speed = 1.75
                        self.charging = False
                        self.timeUntilCharge = 6 * FRAMES_PER_SECOND
                
                    self.velocity.makeNormal()
                    self.velocity *= self.speed
                
                self.currentSequence = 1
                self.stunned -= 1

                if not self.stunned:
                    self.textGroup.add(self.eye)
                    self.animation_list.play("idle")
                if not self.stunned % 4:
                    puffsToCreate = 4
                    
                    while puffsToCreate and settings_list[PARTICLES]:
                        puffsToCreate -= 1
                        tempPuff = particle.smokeParticle(self.position,
                                                                 [1,0])
                        tempPuff.velocity.setAngle(359 * random.random())
                        self.effectsGroup.add(tempPuff)

            else:
                self.currentSequence = 0
                self.processAI()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gaveBonus:
                self.world.giveBonus()
                self.gaveBonus = True


    def placeEye(self):
        self.eye.position[0] = self.position[0]
        self.eye.position[1] = self.position[1] - 10

        self.eye.position = (self.target.position - self.eye.position).makeNormal() * 10
        self.eye.position += self.position
        self.eye.position[1] -= 10



    def bulletCollide(self, bullet):
        utility.play_sound(self.bulletSound, BAAKE_CHANNEL)

        if bullet.collideStyle == COLLIDE_STYLE_HURT:
            bullet.die()
        
        elif bullet.collideStyle == COLLIDE_STYLE_REFLECT:
            if bullet.position.x < self.position.x - 64:
                bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                bullet.velocity *= [-1.0, 1.0]
            elif bullet.position.x > self.position.x + 64:
                bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                bullet.velocity *= [-1.0, 1.0]
            if bullet.position.y < self.position.y - 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                bullet.velocity *= [1.0, -1.0]
            elif bullet.position.y > self.position.y + 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                bullet.velocity *= [1.0, -1.0]

        elif bullet.collideStyle == COLLIDE_STYLE_NOVA:
            if not self.stunned:
                self.stunned = 2 * FRAMES_PER_SECOND
                self.hurt(1)
                self.eye.kill()
    

    def hurt(self,damage):
        self.health -= damage
        utility.play_sound(self.hurtSound, BOSS_CHANNEL)
        self.animation_list.play("hurt")

        if self.health <= self.world.level and self.health != 0:
            self.enemyGroup.add(yurei.Yurei(self.groupList))

        if self.health <= 0:
            for actor in self.enemyGroup:
                actor.leaveScreen = True

    def processAI(self):
        if self.health <= self.world.level + 1:
            if self.charging:
                self.speed -= 0.2
                if self.speed <= 1.75:
                    self.speed = 1.75
                    self.charging = False
                    self.textGroup.add(self.eye)
                    self.timeUntilCharge = 7 * FRAMES_PER_SECOND
            else:
                if not self.timeUntilCharge:
                    self.charging = True
                    self.speed = 10
                    self.eye.kill()
                
                self.timeUntilCharge -= 1
                aitools.goToTarget(self,self.target)


        else:
            aitools.goToTarget(self, self.target)



    def die(self):
        self.stunned -= 1
        self.velocity[1] += .1
        self.world.pauseSpawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffsToCreate = 4
            
            while puffsToCreate and settings_list[PARTICLES]:
                puffsToCreate -= 1
                tempPuff = particle.smokeParticle(self.position,
                                                         [1,0])
                tempPuff.velocity.setAngle(359 * random.random())
                self.effectsGroup.add(tempPuff)



    def custom_bounds(self):
        if self.health <= 0:
            self.kill()
            self.eye.kill()
            self = None



    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            if not self.stunned:
                self.object_collided_with.hurt(1)
            
            if self.object_collided_with.position.x < self.position.x - 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x - 112,
                                                                     self.object_collided_with.position.y)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [-1.0, 1.0]
                       
            elif self.object_collided_with.position.x > self.position.x + 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x + 112,
                                                                     self.object_collided_with.position.y)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [-1.0, 1.0]
                    
            if self.object_collided_with.position.y < self.position.y - 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                     self.position.y - 138)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [1.0, -1.0]
                    
            elif self.object_collided_with.position.y > self.position.y + 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                     self.position.y + 170)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [1.0, -1.0]


####################################################
"""    """    """     BOSS TUT     """    """    """
####################################################
####################################################
"""    """    """     BOSS TUT     """    """    """
####################################################
class BossTut(actor.Actor):
    MasterAnimationList = animation.Animation()
    def __init__(self, world, target, groupList):

        """   COMMON VARIABLES   """
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_BOSS      
        
        self.animation_list = copy.copy(self.MasterAnimationList)
        self.animation_list.set_parent(self)
        self.animation_list.play("idle")
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_REFLECT
        self.bounds = [0,0,SCREEN_WIDTH,SCREEN_HEIGHT]
                
        self.canCollide = True
        self.hitrect = pygame.Rect(0,0,106,130)
        
        self.position = vector.Vector2d(-32, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d.zero
        
        """   UNIQUE VARIABLES   """
        self.target = target
        self.world = world
        self.lifeTimer = 0

        self.speed = 5
        self.health = self.world.level + 2
        
        self.sequenceList = [[0]]

        self.stunned = 0

        self.powerupGroup = groupList[POWERUP_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]

        self.gaveBonus = False

        """    AI VARIABLES    """
        self.spinning = False
        self.timeUntilSpin = 0
        self.targetPoint = None

        self.changeDirection = 0

        self.emitter = particle.particleEmitter(vector.Vector2d.zero, vector.Vector2d(60.0, 5.0),
                                                self.effectsGroup,
                                                ["rain"],
                                                270.0, 45.0,
                                                0.0, 0.0,
                                                3.0, 2.0,
                                                -1.0)
        
        self.emitter.mountTo(self, vector.Vector2d(0.0, 50.0))

    def actor_update(self):
        if not self.stunned:
            try:
                self.emitter.update()
            except:
                pass
            
            
        utility.play_music(self.music, True)
        if not self.active and self.health > 0:
            self.active = True

        if self.lifeTimer <= 30 * FRAMES_PER_SECOND and self.health == self.world.level + 2:
            if self.lifeTimer == 30 * FRAMES_PER_SECOND:
                tempImage = self.howToKill
                
                helpBubble = infoBubble.infoBubble(tempImage, self.target,5 * FRAMES_PER_SECOND)
                helpBubble.offset = vector.Vector2d(0.0, -100.0)
                self.textGroup.add(helpBubble)
            self.lifeTimer += 1

        if self.active:
            if self.stunned:
                self.stunned -= 1

                if not self.stunned % 4:
                    puffsToCreate = 4
                    
                    while puffsToCreate and settings_list[PARTICLES]:
                        puffsToCreate -= 1
                        tempPuff = particle.smokeParticle(self.position,
                                                                 [1,0])
                        tempPuff.velocity.setAngle(359 * random.random())
                        self.effectsGroup.add(tempPuff)

                if not self.stunned:
                    self.animation_list.play("idle")

            else:
                self.currentSequence = 0
                self.processAI()

        if self.health <= 0:
            self.active = False
            self.die()
            
            if not self.gaveBonus and self.world.worldName != "Tutorial":
                self.world.giveBonus()
                self.gaveBonus = True


    def bulletCollide(self, bullet):
        utility.play_sound(self.bulletSound, BAAKE_CHANNEL)

        if bullet.collideStyle == COLLIDE_STYLE_HURT:
            bullet.die()
        
        elif bullet.collideStyle == COLLIDE_STYLE_REFLECT:
            if bullet.position.x < self.position.x - 64:
                bullet.position = vector.Vector2d(self.position.x - 112, bullet.position.y)
                bullet.velocity *= [-1.0, 1.0]
            elif bullet.position.x > self.position.x + 64:
                bullet.position = vector.Vector2d(self.position.x + 112, bullet.position.y)
                bullet.velocity *= [-1.0, 1.0]
            if bullet.position.y < self.position.y - 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y - 14)
                bullet.velocity *= [1.0, -1.0]
            elif bullet.position.y > self.position.y + 64:
                bullet.position = vector.Vector2d(bullet.position.x, self.position.y + 140)
                bullet.velocity *= [1.0, -1.0]

        elif bullet.collideStyle == COLLIDE_STYLE_NOVA:
            if not self.stunned:
                self.stunned = 2 * FRAMES_PER_SECOND
                self.hurt(1)


    def hurt(self,damage):
        self.health -= damage
        self.animation_list.play("hurt")
        utility.play_sound(self.hurtSound, BOSS_CHANNEL)

        if self.health <= 0:
            for actor in self.enemyGroup:
                actor.leaveScreen = True

    def processAI(self):
        if self.health <= self.world.level:
            if self.spinning:
                self.bound_style = BOUND_STYLE_NONE
                self.speed += 0.15

                if self.speed > 25:
                    self.spinning = False
                    self.speed = 5
                    self.timeUntilSpin = 8 * FRAMES_PER_SECOND
                    self.bound_style = BOUND_STYLE_REFLECT
            
                self.velocity += self.velocity.getPerpendicular().makeNormal()
                self.velocity = self.velocity.makeNormal() * self.speed

            else:
                if not self.timeUntilSpin:
                    self.spinning = True
                
                else:
                    self.standardBehavior()

                self.timeUntilSpin -= 1

        else:
            self.standardBehavior()



    def standardBehavior(self):
        if not self.changeDirection:
            self.targetPoint = vector.Vector2d(
                                random.randint(
                                 int(self.target.position[0] - 300),
                                 int(self.target.position[0] + 300)),
                                random.randint(
                                 int(self.target.position[1] - 300),
                                 int(self.target.position[1] + 300)))
            self.changeDirection = 30

        self.changeDirection -= 1
        aitools.arcToPoint(self, self.targetPoint,0.5)


    def die(self):
        self.emitter = None
        
        if self.world.worldName == "Tutorial":
            self.world.bossDead = True

        self.velocity[1] += .1
        self.bound_style = BOUND_STYLE_CUSTOM

        self.stunned -= 1
        self.world.pauseSpawning = 1 * FRAMES_PER_SECOND

        if settings_list[PARTICLES] and not self.stunned % 2:
            puffsToCreate = 4
            
            while puffsToCreate and settings_list[PARTICLES]:
                puffsToCreate -= 1
                tempPuff = particle.smokeParticle(self.position,
                                                         [1,0])
                tempPuff.velocity.setAngle(359 * random.random())
                self.effectsGroup.add(tempPuff)



    def custom_bounds(self):
        if self.health <= 0:
            self.kill()
            self = None


    def collide(self):
        if self.object_collided_with.actorType == ACTOR_PLAYER:
            if not self.stunned:
                self.object_collided_with.hurt(1)
            
            if self.object_collided_with.position.x < self.position.x - 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x - 112,
                                                                     self.object_collided_with.position.y)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [-1.0, 1.0]
                       
            elif self.object_collided_with.position.x > self.position.x + 64:
                self.object_collided_with.position = vector.Vector2d(self.position.x + 112,
                                                                     self.object_collided_with.position.y)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [-1.0, 1.0]
                    
            if self.object_collided_with.position.y < self.position.y - 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                     self.position.y - 138)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [1.0, -1.0]
                    
            elif self.object_collided_with.position.y > self.position.y + 64:
                self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x,
                                                                     self.position.y + 170)
                if self.object_collided_with.velocity:
                    self.object_collided_with.velocity *= [1.0, -1.0]