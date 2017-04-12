import copy
import random

from core import enemy
from core.actor import *
from utils import aitools, utility


def load_data():
    Batto.last_spawn = 0, 0
    Batto.death_sound = utility.load_sound('pop')
    Batto.master_animation_list.build_animation('Idle', ['batto'])


class Batto(enemy.Enemy):
    death_sound = None
    master_animation_list = animation.Animation()

    def __init__(self, group_list, leader=None):
        # COMMON VARIABLES
        enemy.Enemy.__init__(self)
        self.actor_type = ACTOR_TYPE_ENEMY
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -32, -32, (SCREEN_WIDTH + 32), (SCREEN_HEIGHT + 32)
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,80,66)
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.speed = 10
        self.change_direction = 0
        self.target = 0, 0
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 1
        self.boss_fight = False
        self.drop_item = False
        
        # EXIT GAME VARIABLES
        self.on_screen = 0
        self.dead = False

        if not leader:
            self.leader = self
            aitools.spawn_off_screen(self, 128)
            Batto.last_spawn = self.position

        else:
            self.leader = leader
            aitools.spawn_at_point(self, Batto.last_spawn)

    def actor_update(self):
        if self.active:
            if self.health <= 0:
                self.die()

            self.on_screen += 1
            self.process_ai()

            if not self.leader.active:
                self.leader = self
        else:
            self.active = True

    def process_ai(self):
        if self.leader.dead:
            pass

        elif self.leader.active and self.leader != self:
            temp_velocity = vector.Vector2d(self.leader.velocity[0], self.leader.velocity[1])
            target_point = self.leader.position - (temp_velocity.make_normal()) * vector.Vector2d(150, 150)
            aitools.go_to_point(self, target_point)

        else:
            if not self.change_direction:
                self.target = vector.Vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                self.change_direction = 30

            self.change_direction -= 1
            aitools.arc_to_point(self, self.target)

    def custom_bounds(self):
        if self.on_screen > FRAMES_PER_SECOND:
            self.active = False
            self.dead = True

        self.on_screen = 0
        
        if self.dead:
            self.kill()

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)
