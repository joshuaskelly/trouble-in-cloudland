from utils import vector
from utils.utility import *


class Text(pygame.sprite.Sprite):
    def __init__(self, font_type, font_size=12, color=(0, 0, 0), text='', life_timer=-1, text_index=0):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        
        self.text_index = text_index
        self.text = text
        self.color = color
        self.font_type = font_type
        self.font_size = font_size
        self.life_timer = life_timer
        self.alignment = TOP_LEFT
        self.font_object = None
        self.image = None
        self.rect = None

        self.build_image()
        self.position = vector.Vector2d(0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if not (self.life_timer == -1):
            if not self.life_timer:
                self.kill()
    
            self.life_timer -= 1
            
        if self.alignment == TOP_LEFT:
            self.rect.topleft = (self.position.x, self.position.y)
        
        elif self.alignment == TOP_MIDDLE:
            self.rect.midtop = (self.position.x, self.position.y)
        
        elif self.alignment == TOP_RIGHT:
            self.rect.topright = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_LEFT:
            self.rect.midleft = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_MIDDLE:
            self.rect.center = (self.position.x, self.position.y)
        
        elif self.alignment == CENTER_RIGHT:
            self.rect.midright = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_LEFT:
            self.rect.bottomleft = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_MIDDLE:
            self.rect.midbottom = (self.position.x, self.position.y)

        elif self.alignment == BOTTOM_RIGHT:
            self.rect.bottomright = (self.position.x, self.position.y)

    def set_font(self, font_size, color, font_type):
        self.color = color
        self.font_type = font_type
        self.font_size = font_size
        self.build_image()

    def set_text(self, text):
        self.text = text
        self.build_image()
    
    def get_text(self):
        return self.text

    def set_color(self, (r, g, b)):
        self.color = r, g, b
    
    def get_color(self):
        return self.color
        
    def get_position(self):
        # This method returns the sprite's position
        return self.position.x, self.position.y

    def set_position(self, (x, y)):
        # This method sets the sprite's position
        self.position.x = x
        self.position.y = y

    def mouse_over(self):
        mouse_position = list(pygame.mouse.get_pos())

        if (mouse_position[0] > self.rect.left) and (mouse_position[0] < self.rect.right) and (mouse_position[1] > self.rect.top) and (mouse_position[1] < self.rect.bottom):
            return True

        else:
            return False
        
    def mouse_over_dump(self):
        print 'Mouse Position: ', list(pygame.mouse.get_pos())
        print '[Rect Dimensions: ', '<LEFT: ', self.rect.left, '>', '<RIGHT: ', self.rect.right, '>', '<TOP: ', self.rect.top, '>', '<BOTTOM: ', self.rect.bottom, '>]'

    def set_timer(self, life_timer):
        self.life_timer = life_timer
    
    def set_alignment(self, alignment):
        self.alignment = alignment

    def copy(self):
        new_object = Text(self.font_type, self.font_size, self.color, self.text, self.life_timer)
        new_object.set_alignment(self.alignment)
        
        return new_object

    def build_image(self):
        self.font_object = pygame.font.Font(self.font_type, self.font_size)
        self.image = self.font_object.render(str(self.text), ANTI_ALIAS, self.color)
        self.rect = self.image.get_rect()


class TextSurface(object):
    def __init__(self,fontType,fontSize,color,text):
        font_object = pygame.font.Font(fontType, fontSize)
        self.image = font_object.render(str(text), ANTI_ALIAS, color)
