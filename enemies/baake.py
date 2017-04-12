import copy

from core import actor
from core.actor import *
from utils import aitools, utility


def load_data():
    Baake.bullet_sound = utility.load_sound('baakeHit')
    Baake.master_animation_list.build_animation('Idle', ['baake'])


class Baake(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        #   COMMON VARIABLES
        actor.Actor.__init__(self)
        self.actor_type = ACTOR_TYPE_BAAKE
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        
        self.rect = self.image.get_rect()
        
        self.bound_style = BOUND_STYLE_REFLECT
        self.bounds = 32, 32, SCREEN_WIDTH - 32, SCREEN_HEIGHT - 32
                
        self.can_collide = True
        self.hitrect = pygame.Rect(0,0,108,88)
        
        self.position = vector.Vector2d(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = vector.Vector2d(5.0, 0.0)
        
        # UNIQUE VARIABLES
        self.speed = 5.0
        self.change_direction = 0

        # BOSS FIGHT
        self.leave_screen = False

        aitools.spawn_on_screen(self)

    def actor_update(self):
        if not self.leave_screen:
            self.process_ai()

        else:
            self.bound_style = BOUND_STYLE_KILL

        if not self.active:
            self.active = True
        
    def process_ai(self):
        if not self.change_direction:
            self.change_direction = 2 * FRAMES_PER_SECOND
            aitools.cardinal_direction(self)
                
        self.change_direction -= 1
    
    def collide(self):
        if self.object_collided_with.actor_type == ACTOR_BULLET:
            utility.play_sound(Baake.bullet_sound, BAAKE_CHANNEL)

        elif self.object_collided_with.actor_type == ACTOR_PLAYER:
                if self.object_collided_with.position.x < self.position.x - 64:
                    self.object_collided_with.position = vector.Vector2d((self.position.x - 94), self.object_collided_with.position.y)

                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= -1.0, 1.0
                           
                elif self.object_collided_with.position.x > self.position.x + 64:
                    self.object_collided_with.position = vector.Vector2d((self.position.x + 94), self.object_collided_with.position.y)

                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= -1.0, 1.0
                        
                if self.object_collided_with.position.y < self.position.y - 32:
                    self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y - 76)

                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= 1.0, -1.0
                        
                elif self.object_collided_with.position.y > self.position.y + 32:
                    self.object_collided_with.position = vector.Vector2d(self.object_collided_with.position.x, self.position.y + 108)

                    if self.object_collided_with.velocity:
                        self.object_collided_with.velocity *= 1.0, -1.0
