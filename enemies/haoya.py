import copy

import pygame

from core import animation, enemy, particle
from utils import aitools, utility, vector
from utils.settings import *


def load_data():
    Haoya.death_sound = utility.load_sound('pop')
    Haoya.master_animation_list.build_animation('Idle', ['haoya'])


class Haoya(enemy.Enemy):
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
        self.hitrect = pygame.Rect(0, 0, 54, 58)
        self.hitrect_offset_y = 6
        self.velocity = vector.Vector2d.zero
        
        # UNIQUE VARIABLES
        self.speed = 2
        self.target = target_object
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 3
        self.boss_fight = False
        self.drop_item = False
        
        self.death_emitter = particle.ParticleEmitter(vector.Vector2d.zero,
                                                      self.effects_group,
                                                      ['puff'],
                                                      0.0, 360.0,
                                                      5.0, 0.0,
                                                      1.0, 4.0,
                                                      -1.0)
        
        self.death_emitter.mount_to(self)
        
        #  LEAVE SCREEN VARIABLES 
        self.life_timer = 10 * FRAMES_PER_SECOND
        self.leave_screen = False
        
        aitools.spawn_off_screen(self)

    def process_ai(self):
        if self.leave_screen:
            pass

        elif self.active:
            # Find the distance to the player
            magnitude = self.target.position - self.position
            if magnitude.get_magnitude() < 250:
                # If the player is within x distance then charge the player.
                self.speed = 7
            else:
                self.speed = 2

            aitools.go_to_target(self, self.target)

    def actor_update(self):
        self.life_timer -= 1
        
        if not self.life_timer:
            self.leave_screen = True
            self.speed = 7
            aitools.go_to_point(self, aitools.point_off_screen())

        if self.active and self.health <= 0:
            self.active = False
            self.die()
        
        if not self.active and self.health:
            self.active = True

        self.process_ai()

    def custom_bounds(self):
        if self.leave_screen:
            self.kill()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
