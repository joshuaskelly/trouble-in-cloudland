import baake
import boss
import infobubble
import moono
import text
import utility
import vector
from settings import *


class Tutorial:
    def __init__(self, (world_name, player, group_list)):
        self.timer = 0
        self.boss_fight = False
        self.time_after_boss = 0
        self.boss_dead = False
        self.moono_dead = True
        self.mass_attack = False
        self.default_spawn_rate = 0
        self.moono_spawn_rate = 0
        self.force_drop = 0
        self.level = 0
        self.world_name = world_name
        self.player = player
        self.text_group = group_list[TEXT_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.boss_group = group_list[BOSS_GROUP]
        self.group_list = group_list
        self.current_step = 0
        self.new_moono = moono.Moono(self.player, self.group_list)

    def update(self):
        if self.boss_dead:
            self.time_after_boss += 1

        if self.default_spawn_rate:
            if not self.moono_spawn_rate:
                self.moono_spawn_rate = self.default_spawn_rate
                self.spawn_moono()

            self.moono_spawn_rate -= 1

        if self.new_moono.health <= 0:
            self.moono_dead = True

        if self.current_step == 0:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Welcome to the tutorial!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.current_step += 1
            self.timer = 0
            
        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 1:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Use your mouse to move.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 5 * FRAMES_PER_SECOND and self.current_step == 2:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Notice the stars that you shoot?').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 3:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'When moving you shoot stars.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 4:
            self.spawn_moono('balloon')
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Oh no! Its a Moono!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1
        
        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 5:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Attack with your stars!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 6:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Moonos hurt you when they touch you.').image
            self.timer -= 1
            self.moono_dead = False
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 7:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Did you get the Balloon?').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 8:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Collect balloons for bonus points!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 9:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Balloons always help you get more points.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 10:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Points are important!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 11:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Every 50,000 points you get an extra life!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 12:
            self.spawn_baake()
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Oh bother! It's Baake.").image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 13:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Baakes don't hurt you...").image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 14:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, '...but they do love to get in the way!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 15:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Its usually best to stay away from Baake.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 16:
            self.spawn_moono('reflect')
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Blast, another Moono!').image
            self.moono_dead = False
            self.timer-= 1
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 17:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Did you pickup that powerup gem?').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 18:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Gems change how you attack.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 19:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "These effects don't last long...").image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 20:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, '...but they do stack!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 21:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'So pick up as many as you can!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 22:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'It is important to make use of gems').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 23:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'They can really help you out!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 24:
            self.default_spawn_rate = 2.5 * FRAMES_PER_SECOND
            self.mass_attack = True
            self.timer = 0
            self.current_step +=1

        if self.current_step == 25:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "They're attacking en masse!").image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 26:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Try moving slowly towards them.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 27:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'You can better control your shots.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 28:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'This can really increase your chances!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 3 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1


        if self.timer >= 4 * FRAMES_PER_SECOND and self.current_step == 29:
            self.spawn_boss()
            self.boss_fight = True
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Oh no! Its a boss!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 30:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Kill the moonos that spawn.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer >= 3 * FRAMES_PER_SECOND and self.current_step == 31:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Some of them will drop a nova.').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer == 3 * FRAMES_PER_SECOND and self.current_step == 32:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Use the nova when the boss is near').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1

        if self.timer == 3 * FRAMES_PER_SECOND and self.current_step == 33:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Only novas can hurt bosses!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)
            self.timer = 0
            self.current_step +=1
        
        if self.time_after_boss == 1 * FRAMES_PER_SECOND:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, 'Congratulations!').image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)

        if self.time_after_boss == 3 * FRAMES_PER_SECOND:
            temp_image = text.TextSurface(FONT_PATH, 30, FONT_COLOR, "Looks like you're ready for a real challenge!").image
            help_bubble = infobubble.InfoBubble(temp_image, self.player, 2 * FRAMES_PER_SECOND)
            help_bubble.set_offset(vector.Vector2d(0.0, -100.0))
            self.text_group.add(help_bubble)

        if self.moono_dead or self.mass_attack:
            self.timer += 1

        if self.time_after_boss == 5 * FRAMES_PER_SECOND:
            utility.fade_music()
            return True

    def spawn_baake(self):
        self.enemy_group.add(baake.Baake())

    def spawn_moono(self, force_drops = None):
        self.new_moono = moono.Moono(self.player,
                                     self.group_list)
        
        if force_drops:
            self.new_moono.boss_fight = True
            
            if force_drops == 'reflect':
                self.new_moono.drop_reflect = True

            if force_drops == 'balloon':
                self.new_moono.drop_balloon = True

        elif self.boss_fight:
            self.force_drop += 1
            self.new_moono.boss_fight = True

            if self.force_drop > 4:
                self.new_moono.drop_item = True
                self.force_drop = 0

        self.enemy_group.add(self.new_moono)

    def spawn_boss(self):
        self.boss_group.add(boss.BossTut(self, self.player, self.group_list))
