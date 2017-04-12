import actor
import utility

from actor import *


class InfoBubble(actor.Actor):
    def __init__(self, surface, target, life_timer = -1):
        actor.Actor.__init__(self)
        
        self.surface = surface
        self.surface_rect = self.surface.get_rect()
        self.mounted = False
        self.target = target
        self.image = None
        self.balloon_pointer_down = utility.load_image('balloonPointerDown')
        self.balloon_pointer_up = utility.load_image('balloonPointerUp')
        self.balloon_pointer_direction = 'Down'
        self.rect = None
        self.velocity = vector.Vector2d.zero
        self.bounds = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        self.bound_style = BOUND_STYLE_CUSTOM
        self.offset = vector.Vector2d.zero
        self.life_timer = life_timer
        self.position = target.position + self.offset
        self.mounted = True
        self.balloon_pointer_rect = None

        self.create_bubble()
        self.update()
    
    def actor_update(self):
        if self.life_timer:
            if self.mounted:
                self.position = self.target.position + self.offset + vector.Vector2d(self.target.hitrect_offset_x, self.target.hitrect_offset_y)
            
            self.life_timer -= 1
            
        if not self.life_timer:
            self.die()
            
    def set_offset(self, offSet):
        self.offset = offSet
        self.position += self.offset

    def create_bubble(self):
        white_box = pygame.Surface((self.surface.get_width() + 6, self.surface.get_height() + 6))
        white_box.fill((255,255,255))
        white_box_rect = white_box.get_rect()
        dark_box = pygame.Surface((self.surface.get_width() + 14, self.surface.get_height() + 14))
        dark_box.fill(FONT_COLOR)
        dark_box_rect = dark_box.get_rect()
        
        self.balloon_pointer_rect = self.balloon_pointer_down.get_rect()
        
        self.image = pygame.Surface((dark_box.get_width(), dark_box.get_height() + 38))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
        dark_box_rect.center = self.rect.center
        white_box_rect.center = dark_box_rect.center
        self.surface_rect.center = white_box_rect.center
        self.balloon_pointer_rect.center = white_box_rect.center
        
        self.image.blit(dark_box,dark_box_rect)
        self.image.blit(white_box,white_box_rect)
        self.image.blit(self.surface, self.surface_rect)
        
        if self.offset.y <= 0 and self.balloon_pointer_direction == 'Down':
            self.balloon_pointer_rect.top = white_box_rect.bottom
            self.image.blit(self.balloon_pointer_down, self.balloon_pointer_rect)
            self.balloon_pointer_direction = 'Up'

        if self.offset.y > 0 and self.balloon_pointer_direction == 'Up':
            self.balloon_pointer_rect.bottom = white_box_rect.top
            self.image.blit(self.balloon_pointer_up, self.balloon_pointer_rect)
            self.balloon_pointer_direction = 'Down'
        
        self.bounds = self.image.get_width() / 2, self.image.get_height() / 2 , SCREEN_WIDTH - (self.image.get_width() / 2), SCREEN_HEIGHT - (self.image.get_height() / 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def custom_bounds(self):
        if self.position.y < self.bounds[TOP] or self.position.y > self.bounds[BOTTOM]:
            self.offset *= -1
            self.create_bubble()
            
        if self.position.x < self.bounds[LEFT]:
            self.position = vector.Vector2d(self.bounds[LEFT], self.position.y)

        elif self.position.x > self.bounds[RIGHT]:
            self.position = vector.Vector2d(self.bounds[RIGHT], self.position.y)
