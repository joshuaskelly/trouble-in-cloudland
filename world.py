import pygame

import baake
import batto
import bokko
import boss
import hakta
import haoya
import infobubble
import moono
import paajo
import raayu
import rokubi
import text
import utility
import vector
import yurei
from settings import *


def load_data():
    World.bonus_tally_sound = utility.load_sound('bonusTally')
    World.boss_fight_music = utility.load_sound('bossMusic')
    World.get_ready_sound = utility.load_sound('getReady')

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
    def __init__(self, (world_name, player, group_list, level_list), music):
        self.world_name = world_name
        self.player = player
        self.music = music
        self.group_list = group_list
        self.powerup_group = group_list[POWERUP_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.boss_group = group_list[BOSS_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.stage_score = 0
        self.level_list = level_list
        self.level = 0
        self.stage = 0
        self.done = False
        self.enemy_list = []
        self.defeat_stage = None

        # ROKUBI VARIABLES
        self.rokubi_group = pygame.sprite.Group()

        # BOSS FIGHT VARIABLES
        self.pause_spawning = 0
        self.boss_fight = False
        self.force_drop = 0
        self.bonus_text = None
        self.bonus_amount = None
        self.bonus = -1
        self.after_bonus_pause = 0

    def load(self):
        self.load_level()
        self.player.increment_score_no_text(0)

    def load_level(self):
        if self.done:
            return

        utility.fade_music()
        utility.play_music(self.music, True)
        self.stage = 0
        self.pause_spawning = 3 * FRAMES_PER_SECOND
        self.player.bullet_bonus = 0
        self.player.reflect_bonus = 0

        self.powerup_group.empty()
        self.enemy_group.empty()
        self.effects_group.empty()

        # Display Level text
        display_name = text.Text(FONT_PATH, 64, FONT_COLOR, self.world_name, 90)
        display_name.set_alignment(CENTER_MIDDLE)
        display_name.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.group_list[TEXT_GROUP].add(display_name)

        display_level = text.Text(FONT_PATH, 32, FONT_COLOR, 'Level ' + str(self.level + 1), 90)
        display_level.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT * (2.0 / 3.0)))
        display_level.set_alignment(CENTER_MIDDLE)
        self.group_list[TEXT_GROUP].add(display_level)

        # Reset all information for the new level
        self.enemy_list = []
        self.load_stage()

        utility.play_sound(self.get_ready_sound, OW_CHANNEL)

        temp_image = text.TextSurface(FONT_PATH, 36, FONT_COLOR, 'Get Ready...').image
        help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
        help_bubble.offset = vector.Vector2d(0.0, -100.0)
        self.effects_group.add(help_bubble)

    def load_boss(self):
        self.enemy_list = []

        for enemy in self.level_list[self.level]:
            if enemy[STAGE_SPAWNED] == self.stage:
                while enemy[DEFAULT_SPAWN]:
                    enemy[DEFAULT_SPAWN] -= 1
                    self.create_actor(enemy[ACTOR_TYPE])

            if enemy[STAGE_SPAWNED] == self.stage:
                # Time until spawn, actor type, spawn rate
                self.enemy_list.append([0, enemy[ACTOR_TYPE], enemy[SPAWN_RATE]])

    def give_bonus(self):
        increment_bonus = self.player.lives * 50

        if self.bonus == -1:
            self.boss_fight = False
            self.bonus = 0
            self.bonus_text = text.Text(FONT_PATH, 64, FONT_COLOR, 'Bonus Points!')
            self.bonus_text.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            self.bonus_text.set_alignment(CENTER_MIDDLE)
            self.text_group.add(self.bonus_text)

            self.bonus_amount = text.Text(FONT_PATH, 48, FONT_COLOR)
            self.bonus_amount.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
            self.bonus_amount.set_alignment(CENTER_MIDDLE)
            self.text_group.add(self.bonus_amount)

        if self.bonus < self.player.lives * 5000 - increment_bonus:
            self.bonus += increment_bonus
            self.bonus_amount.set_text(self.bonus)

        else:
            self.bonus_amount.set_text(self.player.lives * 5000)

            if self.level < MAX_LEVEL:
                self.bonus_text.set_timer(FRAMES_PER_SECOND)
                self.bonus_amount.set_timer(FRAMES_PER_SECOND)

            self.bonus = -1
            self.after_bonus_pause = 1.1 * FRAMES_PER_SECOND

            if self.level < MAX_LEVEL:
                self.level += 1

            self.boss_fight = False
            utility.fade_music()
            utility.play_music(self.music, True)

        utility.play_sound(self.bonus_tally_sound, BAAKE_CHANNEL)
        self.player.increment_score_no_text(increment_bonus)
        self.pause_spawning = 1.5 * FRAMES_PER_SECOND

    def boss_text(self):
        utility.fade_music()
        utility.play_music(self.boss_fight_music, True)

        # Display boss text
        display_stage = text.Text(FONT_PATH, 64, FONT_COLOR, 'Boss Fight!', 90)
        display_stage.position = vector.Vector2d((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        display_stage.set_alignment(CENTER_MIDDLE)
        self.text_group.add(display_stage)

    def load_stage(self):
        # Get player's current score
        self.defeat_stage = DEFEAT_STAGE

        # Display stage text
        if self.stage != 0:
            display_stage = text.Text(FONT_PATH, 32, FONT_COLOR, 'Stage ' + str(self.stage + 1), 90)
            display_stage.position = vector.Vector2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            display_stage.set_alignment(CENTER_MIDDLE)
            self.group_list[TEXT_GROUP].add(display_stage)

        # Enemies spawned here will appear during a level's warm up
        for enemy in self.level_list[self.level]:
            if enemy[STAGE_SPAWNED] == self.stage:
                while enemy[DEFAULT_SPAWN]:
                    enemy[DEFAULT_SPAWN] -= 1
                    self.create_actor(enemy[ACTOR_TYPE])

            if enemy[STAGE_SPAWNED] == self.stage:
                # Time until spawn, actor type, spawn rate
                self.enemy_list.append([0, enemy[ACTOR_TYPE], enemy[SPAWN_RATE]])

    def warmup(self):
        self.pause_spawning -= 1
        
        if not self.pause_spawning:
            if self.boss_fight:
                self.load_boss()
            
            return True
        
        return False

    def update(self):
        if not self.boss_fight:
            utility.play_music(self.music)

        if self.after_bonus_pause >= 1:
            self.after_bonus_pause -= 1
            if self.after_bonus_pause < 1:
                if self.level >= MAX_LEVEL:
                    self.bonus_text.kill()
                    self.bonus_amount.kill()
                    self.done = True

                else:
                    self.load_level()

        if self.done:
            return self.done

        if self.bonus != -1:
            self.give_bonus()

        if self.pause_spawning:
            live = self.warmup()
            
            if not live:
                return

        if not self.boss_fight:
            self.defeat_stage -= 1

            if not self.defeat_stage:
                if self.stage < MAX_STAGE:
                    self.stage += 1
                    self.load_stage()

                else:
                    for enemy in self.enemy_group:
                        if enemy.actor_type == ACTOR_TYPE_BAAKE:
                            enemy.leave_screen = True

                    self.boss_fight = True
                    self.stage += 1
                    self.pause_spawning = 3 * FRAMES_PER_SECOND
                    self.boss_text()

        for enemy in self.enemy_list:
            if enemy[SPAWN_RATE] != -1:
                if not enemy[TIME_TO_SPAWN]:
                    self.create_actor(enemy[ACTOR_TYPE])
                    enemy[TIME_TO_SPAWN] = enemy[SPAWN_RATE]
                
                enemy[TIME_TO_SPAWN] -= 1

    def create_actor(self, actor_type):
        if actor_type == ACTOR_MOONO:
            new_moono = moono.Moono(self.player,
                                    self.group_list)
            if self.boss_fight:
                self.force_drop += 1
                new_moono.boss_fight = True

                if self.force_drop > 10:
                    new_moono.drop_item = True
                    self.force_drop = 0

            self.enemy_group.add(new_moono)

        elif actor_type == ACTOR_ROKUBI:
            spawn = False

            if len(self.rokubi_group) <= 5 and not self.boss_fight:
                spawn = True

            elif len(self.rokubi_group) <= 10 and self.boss_fight:
                spawn = True
            
            if spawn:
                new_rokubi = rokubi.Rokubi(self.player,
                                           self.group_list)
                
                self.rokubi_group.add(new_rokubi)
                
                if self.boss_fight:
                    self.force_drop += 1
                    new_rokubi.boss_fight = True

                    if self.force_drop > 10:
                        new_rokubi.drop_item = True
                        self.force_drop = 0
                
                self.enemy_group.add(new_rokubi)

        elif actor_type == ACTOR_HAOYA:
            new_haoya = haoya.Haoya(self.player, self.group_list)
            
            if self.boss_fight:
                self.force_drop += 1
                new_haoya.boss_fight = True
                if self.force_drop > 10:
                    new_haoya.drop_item = True
                    self.force_drop = 0
            
            self.enemy_group.add(new_haoya)

        elif actor_type == ACTOR_BATTO:
            batto_spawn = 5
            last_batto = None

            while batto_spawn:
                new_batto = batto.Batto(self.group_list, last_batto)
                batto_spawn -= 1
                last_batto = new_batto
            
                if self.boss_fight:
                    self.force_drop += 1
                    new_batto.boss_fight = True

                    if self.force_drop > 19:
                        new_batto.drop_item = True
                        self.force_drop = 0
            
                self.enemy_group.add(new_batto)
        
        elif actor_type == ACTOR_YUREI:
            self.enemy_group.add(yurei.Yurei(self.group_list))

        elif actor_type == ACTOR_HAKTA:
            new_hakta = hakta.Hakta(self.player, self.group_list)

            if self.boss_fight:
                self.force_drop += 1
                new_hakta.boss_fight = True

                if self.force_drop > 10:
                    new_hakta.drop_item = True
                    self.force_drop = 0

            self.enemy_group.add(new_hakta)

        elif actor_type == ACTOR_RAAYU:
            new_raayu = raayu.Raayu(self.player, self.group_list)

            if self.boss_fight:
                self.force_drop += 1
                new_raayu.boss_fight = True

                if self.force_drop > 10:
                    new_raayu.drop_item = True
                    self.force_drop = 0

            self.enemy_group.add(new_raayu)

        elif actor_type == ACTOR_PAAJO:
            paajo_spawn = 5
            paajo_group = []

            while paajo_spawn:
                new_paajo = paajo.Paajo(self.group_list, paajo_spawn)

                paajo_group.append(new_paajo)
                paajo_spawn -= 1

                if self.boss_fight:
                    self.force_drop += 1
                    new_paajo.boss_fight = True

                    if self.force_drop > 19:
                        new_paajo.drop_item = True
                        self.force_drop = 0

            for member in paajo_group:
                member.set_group(paajo_group)
    
            self.enemy_group.add(paajo_group)

        elif actor_type == ACTOR_BAAKE:
            self.enemy_group.add(baake.Baake())

        elif actor_type == ACTOR_BOKKO:
            self.enemy_group.add(bokko.Bokko())

        elif actor_type == ACTOR_BOSS_TUT:
            self.boss_group.add(boss.BossTut(self, self.player, self.group_list))

        elif actor_type == ACTOR_BAAKE_BOSS:
            self.boss_group.add(boss.BaakeBoss(self, self.player, self.group_list))

        elif actor_type == ACTOR_MOONO_BOSS:
            self.boss_group.add(boss.MoonoBoss(self, self.player, self.group_list))
