import infoBubble
import text
import balloon
import gem

import vector
import utility

import moono
import baake
import boss

from settings import *

class Tutorial:
    def __init__(self,(worldName,player,groupList)):
        self.timer = 0
        self.bossFight = False
        self.timeAfterBoss = 0
        self.bossDead = False
        self.moonoDead = True
        self.massAttack = False

        self.defaultSpawnRate = 0
        self.moonoSpawnRate = 0
        self.forceDrop = 0

        self.level = 0
        self.worldName = worldName
        self.player = player
        self.textGroup = groupList[TEXT_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]
        self.bossGroup = groupList[BOSS_GROUP]
        self.groupList = groupList
        
        self.currentStep = 0

        self.newMoono = moono.Moono(self.player,self.groupList)

    def update(self):
        if self.bossDead:
            self.timeAfterBoss += 1

        if self.defaultSpawnRate:
            if not self.moonoSpawnRate:
                self.moonoSpawnRate = self.defaultSpawnRate
                self.spawnMoono()
            self.moonoSpawnRate -= 1

        if self.newMoono.health <= 0:
            self.moonoDead = True

        if self.currentStep == 0:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Welcome to the tutorial!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.currentStep += 1
            self.timer = 0
            
        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 1:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Use your mouse to move.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 5 * FRAMES_PER_SECOND and self.currentStep == 2:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Notice the stars that you shoot?").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)            
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 3:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "When moving you shoot stars.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 4:
            self.spawnMoono("balloon")

            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh no! Its a Moono!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1
        
        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 5:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Attack with your stars!").image

            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 6:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Moonos hurt you when they touch you.").image
            self.timer -= 1
            self.moonoDead = False

            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 7:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Did you get the Balloon?").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 8:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Collect balloons for bonus points!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)    
            self.timer = 0
            self.currentStep +=1            

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 9:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Balloons always help you get more points.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 10:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Points are important!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 11:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Every 50,000 points you get an extra life!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        
        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 12:
            self.spawnBaake()
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh bother! It's Baake.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 13:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Baakes don't hurt you...").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 14:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "...but they do love to get in the way!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 15:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Its usually best to stay away from Baake.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 16:
            self.spawnMoono("reflect")
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Blast, another Moono!").image
            self.moonoDead = False
            self.timer-= 1

            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 17:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Did you pickup that powerup gem?").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 18:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Gems change how you attack.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 19:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "These effects don't last long...").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 20:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "...but they do stack!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 21:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "So pick up as many as you can!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 22:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "It is important to make use of gems").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 23:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "They can really help you out!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 24:
            self.defaultSpawnRate = 2.5 * FRAMES_PER_SECOND
            self.massAttack = True
            self.timer = 0
            self.currentStep +=1

        if self.currentStep == 25:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "They're attacking en masse!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 26:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Try moving slowly towards them.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 27:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "You can better control your shots.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 28:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "This can really increase your chances!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,3 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1


        if self.timer >= 4 * FRAMES_PER_SECOND and self.currentStep == 29:
            self.spawnBoss()
            self.bossFight = True
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh no! Its a boss!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 30:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Kill the moonos that spawn.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.currentStep == 31:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Some of them will drop a nova.").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1

        if self.timer == 3 * FRAMES_PER_SECOND and self.currentStep == 32:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Use the nova when the boss is near").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1


        if self.timer == 3 * FRAMES_PER_SECOND and self.currentStep == 33:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Only novas can hurt bosses!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)
            self.timer = 0
            self.currentStep +=1
        
        if self.timeAfterBoss == 1 * FRAMES_PER_SECOND:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Congratulations!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)

        if self.timeAfterBoss == 3 * FRAMES_PER_SECOND:
            tempImage = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Looks like you're ready for a real challenge!").image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
            helpBubble.setOffSet(vector.Vector2d(0.0, -100.0))
            self.textGroup.add(helpBubble)

        if (self.moonoDead or self.massAttack):
            self.timer += 1

        if self.timeAfterBoss == 5 * FRAMES_PER_SECOND:
            utility.fade_music()
            return True

    def spawnBaake(self):
        self.enemyGroup.add(baake.Baake())

    def spawnMoono(self,forceDrops = None):
        self.newMoono = moono.Moono(self.player,
                                self.groupList)
        
        if forceDrops:
            self.newMoono.bossFight = True
            
            if forceDrops == "reflect":
                self.newMoono.dropReflect = True
            if forceDrops == "balloon":
                self.newMoono.dropBalloon = True

        elif self.bossFight:
            self.forceDrop += 1
            self.newMoono.bossFight = True
            if self.forceDrop > 4:
                self.newMoono.dropItem = True
                self.forceDrop = 0

        self.enemyGroup.add(self.newMoono)

    def spawnBoss(self):
        self.bossGroup.add(boss.BossTut(self,
                                          self.player,
                                          self.groupList))