import copy
import random

from core import enemy
from core.actor import *
from utils import aitools


def load_data():
    Yurei.master_animation_list.build_animation('Idle', ['yurei'])


class Yurei(enemy.Enemy):
    master_animation_list = animation.Animation()

    def __init__(self, groupList):
        enemy.Enemy.__init__(self)

        # COMMON VARIABLES
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = 32, 32, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 32
        self.active = True
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,54,98)
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.speed = 4
        self.target = self
        self.powerup_group = groupList[POWERUP_GROUP]
        self.text_group = groupList[TEXT_GROUP]
        self.effects_group = groupList[EFFECTS_GROUP]
        self.health = -1
        self.change_direction = 0
        self.target_point = vector.Vector2d.zero

        # LEAVE SCREEN VARIABLES
        self.leave_screen = False

        aitools.spawn_off_screen(self)

    def actor_update(self):
        self.health = -1
        if not self.active:
            self.active = True

        self.process_ai()

    def process_ai(self):
        if self.leave_screen:
            pass
        else:
            self.target = aitools.get_closest(self, [self.powerup_group])
    
            if self.target != self and self.target.active:
                aitools.go_to_target(self, self.target)
                self.change_direction = 0
    
            else:
                if not self.change_direction:
                    self.target_point = vector.Vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                    self.change_direction = 30

                self.change_direction -= 1
                aitools.arc_to_point(self, self.target_point)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_TYPE_PICKUP:
            self.object_collided_with.die()

    def custom_bounds(self):
        if self.leave_screen:
            self.kill()
    
    def die(self):
        self.kill()
