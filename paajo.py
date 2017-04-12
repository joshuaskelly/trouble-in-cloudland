import copy
import random

import aitools
import enemy
import utility
from actor import *


def load_data():
    Paajo.death_sound = utility.load_sound('pop')
    Paajo.master_animation_list.build_animation('Idle', ['paajo'])


class Paajo(enemy.Enemy):
    last_spawn = 0, 0
    death_sound = None
    master_animation_list = animation.Animation()

    def __init__(self, group_list, my_position):

        # COMMON VARIABLES
        enemy.Enemy.__init__(self)

        self.actor_type = ACTOR_TYPE_ENEMY
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style = BOUND_STYLE_CUSTOM
        self.bounds = -32, -32, SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,68,74)
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero

        # UNIQUE VARIABLES
        self.speed = 12
        self.change_direction = 0
        self.target = [0,0]
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 2
        self.drop_item = False
        self.boss_fight = False
        self.my_position = my_position
        self.my_flock = None

        # LEAVE SCREEN VARIABLES
        self.life_timer = 5 * FRAMES_PER_SECOND
        self.leave_screen = False

        if self.my_position == 5:
            aitools.spawn_off_screen(self)
            Paajo.last_spawn = self.position
        else:
            aitools.spawn_at_point(self, Paajo.last_spawn)

        if self.my_position == 1:
            self.leader = self

    def actor_update(self):
        self.life_timer -= 1

        if not self.life_timer:
            self.leave_screen = True

        if self.active:
            if self.health <= 0:
                self.die()
                self.active = False
        else:
            self.active = True

        self.process_ai()

    def set_group(self, my_flock):
        self.my_flock = my_flock
        
        for element in self.my_flock:
            if element.my_position == 1:
                self.leader = element

    def process_ai(self):
        if self.leave_screen:
            pass
        
        elif self.my_position != 1:
            flock_chart = [False, False, False, False, False]
            
            for member in self.my_flock:
                if member.active:
                    if member.my_position == self.my_position and member != self and self.my_position < 5:
                        member.my_position += 1

                    flock_chart[member.my_position - 1] = True
                    
                    if member.my_position == 1:
                        self.leader = member

            position_number = 0

            for element in flock_chart:
                position_number += 1

                if position_number < self.my_position and element == False:
                    self.my_position = position_number

                    if self.my_position == 1:
                        self.leader = self

                self.speed = 14.2
                leader_velocity = vector.Vector2d(self.leader.velocity[0], self.leader.velocity[1])
                leader_perpendicular = self.leader.velocity.get_perpendicular()

                if self.my_position % 2:
                    offset = -50

                else:
                    offset = 50

                target_point = self.leader.position - (leader_velocity.make_normal() * 100 * int(self.my_position / 2)) + (leader_perpendicular.make_normal() * offset * int(self.my_position / 2))

                if (target_point - self.position).get_magnitude() < self.speed:
                    aitools.go_to_point(self, target_point)

                else:
                    aitools.arc_to_point(self, target_point, 3)
    
        else:
            for element in self.my_flock:
                if element != self and element.my_position == self.my_position:
                    element.my_position += 1

            self.speed = 11

            if not self.change_direction:
                self.target = vector.Vector2d((random.random() * (SCREEN_WIDTH + 200)) - 100, (random.random() * (SCREEN_HEIGHT + 200)) - 100)
                self.change_direction = 30

            self.change_direction -= 1
            aitools.arc_to_point(self, self.target)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)

    def custom_bounds(self):
        if self.leave_screen:
            self.kill()
