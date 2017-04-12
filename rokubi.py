import copy

import pygame

import aitools
import animation
import enemy
import particle
import utility
import vector
from settings import *


def load_data():
    Rokubi.death_sound = utility.load_sound('pop')
    Rokubi.master_animation_list.build_animation('Idle', ['rokubei'])


class Rokubi(enemy.Enemy):
    death_sound = None
    master_animation_list = animation.Animation()

    def __init__(self, target_object, group_list):
        enemy.Enemy.__init__(self)

        # COMMON VARIABLES
        self.no_spawn = False
        self.actor_type = ACTOR_TYPE_ENEMY
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_NONE
        self.bounds = -32, -32, SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32
        self.can_collide = True
        self.hitrect = pygame.Rect(0, 0, 54, 98)
        self.velocity = vector.Vector2d(0, 0)

        # UNIQUE VARIABLES
        self.speed = 7
        self.hide_behind = target_object
        self.target = target_object
        self.powerup_group = group_list[POWERUP_GROUP]
        self.enemy_group = group_list[ENEMY_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.boss_group = group_list[BOSS_GROUP]
        self.health = 1
        self.drop_item = False
        self.boss_fight = False
        self.charging = False
        self.hiding = False

        self.emitter = particle.ParticleEmitter(vector.Vector2d.zero, vector.Vector2d.zero,
                                                self.effects_group,
                                                ['heart'],
                                                270.0, 45.0,
                                                0.0, 0.0,
                                                8.0, 1.0,
                                                -1.0)
        
        self.emitter.mount_to(self)
        aitools.spawn_off_screen(self)

    def actor_update(self):
        self.emitter.update()
        
        if self.active and self.health <= 0:
            self.health = 0
            self.active = False
            self.die()
        else:
            # This can occasionally cause an error if the rokubi has been
            # removed from the group by an outside function, such as when
            # moving on to a new level.
            if (not self.boss_fight or not self.active and not self.charging) and not self.hiding:
                try:
                    self.hide_behind = aitools.get_closest(self, [self.enemy_group, self.boss_group], [ACTOR_TYPE_BAAKE, ACTOR_TYPE_BOSS])
                    if self.hide_behind == self:
                        self.hide_behind = self.target

                except:
                    self.hide_behind = self.target

            self.active = True

        self.process_ai()

    def process_ai(self):
        self.charging = False

        # Find the distance to the player
        distance = (self.target.position - self.position).get_magnitude()

        if self.hide_behind.actor_type == ACTOR_TYPE_BOSS:
            if distance < 450:
                self.speed = 10
                aitools.go_to_target(self, self.target)
                self.charging = True
                self.hiding = False

        else:
            if distance < 325:
                self.speed = 10
                aitools.go_to_target(self, self.target)
                self.charging = True
                self.hiding = False

        if not self.charging:
            self.speed = 7
            self.hiding = True
            aitools.hide(self, self.hide_behind, self.target)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
