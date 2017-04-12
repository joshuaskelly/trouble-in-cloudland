import copy

import pygame

import aitools
import animation
import balloon
import enemy
import gem
import particle
import utility
import vector
from settings import *


def load_data():
    Moono.death_sound = utility.load_sound('pop')
    Moono.master_animation_list.build_animation('Idle', ['moono'])


class Moono(enemy.Enemy):
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
        self.bound_style = BOUND_STYLE_KILL
        self.bounds = -32, -32, (SCREEN_WIDTH + 32), (SCREEN_HEIGHT + 32)
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,54,98)
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.speed = 3
        self.target = target_object
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 2

        # BOSS FIGHT VARIABLES
        self.boss_fight = False
        self.drop_item = False
        self.drop_balloon = False
        self.drop_reflect = False

        aitools.spawn_away_from_target(self, self.target)

    def actor_update(self):
        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.process_ai()

    def process_ai(self):
        aitools.go_to_target(self, self.target)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)

    def die(self):
        utility.play_sound(self.death_sound)
        particle.DeathEmitter(self.position, self.effects_group).run()

        if self.drop_balloon:
            self.powerup_group.add(balloon.Bonus250(self.position, self.text_group))

        elif self.drop_reflect:
            self.powerup_group.add(gem.Reflect(self.position, self.text_group))

        else:
            self.item_drop()

        self.kill()
        del self
