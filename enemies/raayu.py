import copy

from core import enemy
from core.actor import *
from utils import aitools, utility


def load_data():
    Raayu.death_sound = utility.load_sound('pop')
    Raayu.master_animation_list.build_animation('Idle', ['raayu'])


class Raayu(enemy.Enemy):
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
        self.bounds = -32, -32, SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32
        self.can_collide = True
        self.hitrect = pygame.Rect(0, 0, 66, 82)

        # UNIQUE VARIABLES
        self.speed = 9
        self.target = target_object
        self.powerup_group = group_list[POWERUP_GROUP]
        self.text_group = group_list[TEXT_GROUP]
        self.effects_group = group_list[EFFECTS_GROUP]
        self.health = 2
        self.drop_item = False
        self.boss_fight = False

        # LEAVE SCREEN VARIABLES
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
        aitools.arc_to_point(self, self.target.position, 2)

    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_PLAYER:
            self.object_collided_with.hurt(1)

    def custom_bounds(self):
        if self.leave_screen:
            self.kill()
