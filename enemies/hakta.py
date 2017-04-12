import copy

import pygame

from core import animation, enemy
from utils import aitools, utility, vector
from utils.settings import *


def load_data():
    Hakta.death_sound = utility.load_sound('pop')
    Hakta.master_animation_list.build_animation('Idle', ['hakta'])


class Hakta(enemy.Enemy):
    death_sound = None
    master_animation_list = animation.Animation()

    def __init__(self, target_object, group_list):
        enemy.Enemy.__init__(self)

        # COMMON VARIABLES
        self.actor_type = ACTOR_TYPE_ENEMY
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = 32, 32, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 32
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,106,104)
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.speed = 4
        self.target = target_object
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 2
        self.boss_fight = False
        self.drop_item = False
        
        #  LEAVE SCREEN VARIABLES
        self.life_timer = 5 * FRAMES_PER_SECOND
        self.leave_screen = False
        done = aitools.spawn_off_screen(self)

    def actor_update(self):
        self.life_timer -= 1
        if not self.life_timer:
            self.leave_screen = True

        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.process_ai()

    def process_ai(self):
        if self.leave_screen:
            if self.speed > 5:
                self. speed -= .015

        elif self.speed <= 5:
            self.speed = 13
            aitools.go_to_target(self, self.target)

        else:
            self.speed -= 0.15
            self.velocity = self.velocity.make_normal() * self.speed

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)

    def custom_bounds(self):
        if self.leave_screen:
            self.kill()
