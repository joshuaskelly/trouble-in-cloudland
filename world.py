import utility
import text
import player
import moono
import baake
import batto
import haoya
import rokubi
import yurei
import bokko
import hakta
import raayu
import paajo
import vector
import boss
import pygame
import infoBubble

from settings import *

def loadData():
    World.bonusTally = utility.loadSound("bonusTally")
    World.bossFightMusic = utility.loadSound("bossMusic")
    World.getReady = utility.loadSound("getReady")

"""
Not a dictionary but rather a list of lists.
World.levelList = 
    {level0 = [[stageSpawned, actor-type, maxSpawn_rate, defaultSpawn],[...],...]
    level1[[...],[...]...}

stageSpawned == in which stage of the level
                 does the actor start spawning
actorType == the actor type that is going to
              be added to the spawn list for
              this stage.
maxSpawn_rate == the least number of frames 
                  possible between spawning.
                  Set to -1 to not allow any
                  new spawning.
defaultSpawn == how many of this actor type
                 spawn at the beginning of that
                 stage.
"""
class World:
    def __init__(self,(worldName, player, groupList, levelList), music):
        self.worldName = worldName
        self.player = player

        self.music = music
        self.groupList = groupList

        self.powerupGroup = groupList[POWERUP_GROUP]
        self.enemyGroup = groupList[ENEMY_GROUP]
        self.bossGroup = groupList[BOSS_GROUP]
        self.textGroup = groupList[TEXT_GROUP]
        self.effectsGroup = groupList[EFFECTS_GROUP]

        self.stageScore = 0
        
        self.levelList = levelList
        self.level = 0
        self.stage = 0
        self.done = False

        """    ROKUBI VARIABLES    """
        self.rokubiGroup = pygame.sprite.Group()

        """    BOSS FIGHT VARIABLES    """
        self.pauseSpawning = 0
        self.bossFight = False
        self.forceDrop = 0
        self.bonusText = None
        self.bonusAmount = None
        self.bonus = -1
        self.afterBonusPause = 0



    def load(self):
        self.loadLevel()
        self.player.increment_score_no_text(0)
    
    
    def loadLevel(self):
        if self.done:
            return

        utility.fade_music()
        utility.play_music(self.music, True)
        self.stage = 0
        self.pauseSpawning = 3 * FRAMES_PER_SECOND
        self.player.bulletBonus = 0
        self.player.reflectBonus = 0

        self.powerupGroup.empty()
        self.enemyGroup.empty()
        self.effectsGroup.empty()

        """Display Level text"""
        display_name = text.Text(FONT_PATH, 64, FONT_COLOR, self.worldName, 90)
        display_name.set_alignment(CENTER_MIDDLE)
        display_name.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.groupList[TEXT_GROUP].add(display_name)
        
        displayLevel = text.Text(FONT_PATH, 32, FONT_COLOR, "Level " + str(self.level + 1), 90)
        displayLevel.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT * (2.0 / 3.0)))
        displayLevel.set_alignment(CENTER_MIDDLE)
        self.groupList[TEXT_GROUP].add(displayLevel)

        """Reset all information for the new level"""
        self.enemyList = []
        self.loadStage()

        utility.play_sound(self.getReady, OW_CHANNEL)

        tempImage = text.TextSurface(FONT_PATH, 36, FONT_COLOR, "Get Ready...").image
        
        helpBubble = infoBubble.infoBubble(tempImage, self.player,2 * FRAMES_PER_SECOND)
        helpBubble.offset = vector.Vector2d(0.0, -100.0)
        self.effectsGroup.add(helpBubble)

    
    
    def loadBoss(self):
        self.enemyList = []

        for enemy in self.levelList[self.level]:
            if enemy[STAGE_SPAWNED] == self.stage:
                while enemy[DEFAULT_SPAWN]:
                    enemy[DEFAULT_SPAWN] -= 1
                    self.createActor(enemy[ACTOR_TYPE])
            if enemy[STAGE_SPAWNED] == self.stage:
                """time till spawn, actor type, spawn rate"""
                self.enemyList.append([0, enemy[ACTOR_TYPE], enemy[SPAWN_RATE]])



    def giveBonus(self):
        incrementBonus = self.player.lives * 50

        if self.bonus == -1:
            self.bossFight = False
            self.bonus = 0
            self.bonusText = text.Text(FONT_PATH, 64, FONT_COLOR, "Bonus Points!")
            self.bonusText.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            self.bonusText.set_alignment(CENTER_MIDDLE)
            self.textGroup.add(self.bonusText)

            self.bonusAmount = text.Text(FONT_PATH, 48, FONT_COLOR)
            self.bonusAmount.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
            self.bonusAmount.set_alignment(CENTER_MIDDLE)
            self.textGroup.add(self.bonusAmount)

        if self.bonus < self.player.lives * 5000 - incrementBonus:
            self.bonus += incrementBonus
            self.bonusAmount.set_text(self.bonus)
        else:
            self.bonusAmount.set_text(self.player.lives * 5000)
            if self.level < MAX_LEVEL:
                self.bonusText.setTimer(FRAMES_PER_SECOND)
                self.bonusAmount.setTimer(FRAMES_PER_SECOND)

            self.bonus = -1

            self.afterBonusPause = 1.1 * FRAMES_PER_SECOND

            if self.level < MAX_LEVEL:
                self.level += 1

            self.bossFight = False
            utility.fade_music()
            utility.play_music(self.music, True)

        utility.play_sound(self.bonusTally, BAAKE_CHANNEL)
        self.player.increment_score_no_text(incrementBonus)
        self.pauseSpawning = 1.5 * FRAMES_PER_SECOND



    def bossText(self):
        utility.fade_music()
        utility.play_music(self.bossFightMusic, True)
        """Display boss text"""
        displayStage = text.Text(FONT_PATH, 64, FONT_COLOR, "Boss Fight!", 90)
        displayStage.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        displayStage.set_alignment(CENTER_MIDDLE)
        self.textGroup.add(displayStage)



    def loadStage(self):
        """Get player's current score"""
        self.defeatStage = DEFEAT_STAGE
        
        """Display stage text"""
        if self.stage != 0:
            displayStage = text.Text(FONT_PATH, 32, FONT_COLOR, "Stage " + str(self.stage + 1), 90)
            displayStage.position = vector.Vector2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            displayStage.set_alignment(CENTER_MIDDLE)
            self.groupList[TEXT_GROUP].add(displayStage)

        """Enemies spawned here will appear during a
        level's warm up"""

        for enemy in self.levelList[self.level]:
            if enemy[STAGE_SPAWNED] == self.stage:
                while enemy[DEFAULT_SPAWN]:
                    enemy[DEFAULT_SPAWN] -= 1
                    self.createActor(enemy[ACTOR_TYPE])
            if enemy[STAGE_SPAWNED] == self.stage:
                """time till spawn, actor type, spawn rate"""
                self.enemyList.append([0, enemy[ACTOR_TYPE], enemy[SPAWN_RATE]])



    def warmup(self):
        self.pauseSpawning -= 1
        
        if not self.pauseSpawning:
            if self.bossFight:
                self.loadBoss()
            
            return True
        
        return False



    def update(self):
        if not self.bossFight:
            utility.play_music(self.music)

        if self.afterBonusPause >= 1:
            self.afterBonusPause -= 1
            if self.afterBonusPause < 1:
                if self.level >= MAX_LEVEL:
                    self.bonusText.kill()
                    self.bonusAmount.kill()
                    self.done = True
                else:
                    self.loadLevel()

        if self.done:
            return self.done

        if self.bonus != -1:
            self.giveBonus()

        if self.pauseSpawning:
            live = self.warmup()
            
            if not live:
                return

        if not self.bossFight:
            self.defeatStage -= 1

            if not self.defeatStage:
                if self.stage < MAX_STAGE:
                    self.stage += 1
                    self.loadStage()
                else:
                    for enemy in self.enemyGroup:
                        if enemy.actorType == ACTOR_TYPE_BAAKE:
                            enemy.leaveScreen = True
                    self.bossFight = True
                    self.stage += 1
                    self.pauseSpawning = 3 * FRAMES_PER_SECOND
                    self.bossText()

        for enemy in self.enemyList:
            if enemy[SPAWN_RATE] != -1:
                if not enemy[TIME_TO_SPAWN]:
                    self.createActor(enemy[ACTOR_TYPE])
                    enemy[TIME_TO_SPAWN] = enemy[SPAWN_RATE]
                
                enemy[TIME_TO_SPAWN] -= 1



    def createActor(self, actorType):
        if actorType == ACTOR_MOONO:
            newMoono = moono.Moono(self.player,
                                    self.groupList)
            if self.bossFight:
                self.forceDrop += 1
                newMoono.bossFight = True
                if self.forceDrop > 10:
                    newMoono.dropItem = True
                    self.forceDrop = 0

            self.enemyGroup.add(newMoono)

        elif actorType == ACTOR_ROKUBI:
            spawn = False

            if len(self.rokubiGroup) <= 5 and not self.bossFight:
                spawn = True
            elif len(self.rokubiGroup) <= 10 and self.bossFight:
                spawn = True
            
            if spawn:
                newRokubi = rokubi.Rokubi(self.player,
                                           self.groupList)
                
                self.rokubiGroup.add(newRokubi)
                
                if self.bossFight:
                    self.forceDrop += 1
                    newRokubi.bossFight = True
                    if self.forceDrop > 10:
                        newRokubi.dropItem = True
                        self.forceDrop = 0
                
                self.enemyGroup.add(newRokubi)

        elif actorType == ACTOR_HAOYA:
            newHaoya = haoya.Haoya(self.player,
                                    self.groupList)
            
            if self.bossFight:
                self.forceDrop += 1
                newHaoya.bossFight = True
                if self.forceDrop > 10:
                    newHaoya.dropItem = True
                    self.forceDrop = 0
            
            self.enemyGroup.add(newHaoya)

        elif actorType == ACTOR_BATTO:

            battoSpawn = 5
            lastBatto = None
            while battoSpawn:
                newBatto = batto.Batto(self.groupList, lastBatto)
                battoSpawn -= 1

                lastBatto = newBatto
            
                if self.bossFight:
                    self.forceDrop += 1
                    newBatto.bossFight = True
                    if self.forceDrop > 19:
                        newBatto.dropItem = True
                        self.forceDrop = 0
            
                self.enemyGroup.add(newBatto)
        
        elif actorType == ACTOR_YUREI:
            self.enemyGroup.add(yurei.Yurei(self.groupList))

        elif actorType == ACTOR_HAKTA:
            newHakta = hakta.Hakta(self.player,
                                    self.groupList)
            if self.bossFight:
                self.forceDrop += 1
                newHakta.bossFight = True
                if self.forceDrop > 10:
                    newHakta.dropItem = True
                    self.forceDrop = 0

            self.enemyGroup.add(newHakta)

        elif actorType == ACTOR_RAAYU:
            newRaayu = raayu.Raayu(self.player,
                                    self.groupList)
            if self.bossFight:
                self.forceDrop += 1
                newRaayu.bossFight = True
                if self.forceDrop > 10:
                    newRaayu.dropItem = True
                    self.forceDrop = 0

            self.enemyGroup.add(newRaayu)

        elif actorType == ACTOR_PAAJO:
            paajoSpawn = 5
            paajoGroup = []

            while paajoSpawn:
                newPaajo = paajo.Paajo(self.groupList,paajoSpawn)

                paajoGroup.append(newPaajo)
                paajoSpawn -= 1

                if self.bossFight:
                    self.forceDrop += 1
                    newPaajo.bossFight = True
                    if self.forceDrop > 19:
                        newPaajo.dropItem = True
                        self.forceDrop = 0

            for member in paajoGroup:
                member.setGroup(paajoGroup)
    
            self.enemyGroup.add(paajoGroup)

        elif actorType == ACTOR_BAAKE:
            self.enemyGroup.add(baake.Baake())

        elif actorType == ACTOR_BOKKO:
            self.enemyGroup.add(bokko.Bokko())

        elif actorType == ACTOR_BOSS_TUT:
            self.bossGroup.add(boss.BossTut(self,
                                              self.player,
                                              self.groupList))

        elif actorType == ACTOR_BAAKE_BOSS:
            self.bossGroup.add(boss.BaakeBoss(self,
                                                self.player,
                                                self.groupList))
        elif actorType == ACTOR_MOONO_BOSS:
            self.bossGroup.add(boss.MoonoBoss(self,
                                                self.player,
                                                self.groupList))