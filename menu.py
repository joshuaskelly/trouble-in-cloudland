import copy

import pygame

import actor
import animation
import text
import utility
import vector
from settings import *


def load_data():
    Cursor.master_animation_list.build_animation('Idle', ['cursor'])


class Menu(object):
    def __init__(self, screen, music_list, background_image, bounds, title, menu_dictionary, start_selection=0):
        
        self.screen = screen
        self.bounds = bounds
        self.menu_dictionary = menu_dictionary
        self.title = title
        self.music_list = music_list
        self.background_image = background_image
        self.cursor = Cursor()
        pygame.mouse.set_visible(False)
        self.menu_group = pygame.sprite.Group()
        self.menu_tooltip_group = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.menu_selection_pointer = []
        self.menu_tooltip_pointer = []
        self.current_selection = start_selection
        self.timer = pygame.time.Clock()
        self.menu_beep_sound = utility.load_sound('menuBeep')
        self.menu_forward_sound = utility.load_sound('menuForward')
        self.menu_back_sound = utility.load_sound('menuBack')
        
        index = 0
        
        menu_title = text.Text(FONT_PATH, title[1], FONT_COLOR, title[0])
        menu_title.position = vector.Vector2d(title[2], title[3])
        menu_title.set_alignment(CENTER_MIDDLE)
        self.menu_group.add(menu_title)
        
        for option in menu_dictionary:
            menu_selection = text.Text(FONT_PATH, 32, FONT_INACTIVE_COLOR, menu_dictionary[option][0], -1, index)
            menu_selection.set_alignment(CENTER_MIDDLE)
            menu_selection.position = vector.Vector2d((((self.bounds[RIGHT] - self.bounds[LEFT]) / 2) + self.bounds[LEFT],
                                                      ((self.bounds[BOTTOM]-self.bounds[TOP]) / (len(self.menu_dictionary) + 1) * (index + 1)) + self.bounds[TOP]))
            
            self.menu_group.add(menu_selection)
            self.menu_selection_pointer.append(menu_selection)
            
            menu_tooltip = text.Text(FONT_PATH, 32, FONT_COLOR, menu_dictionary[option][1])
            menu_tooltip.set_alignment(BOTTOM_MIDDLE)
            menu_tooltip.position = vector.Vector2d(((SCREEN_WIDTH / 2), SCREEN_HEIGHT))
            self.menu_tooltip_group.add(menu_tooltip)
            self.menu_tooltip_pointer.append(menu_tooltip)

            index += 1
            
        self.cursor_group.add(self.cursor)

    def show(self):
        self.menu_selection_pointer[self.current_selection].set_font(48, FONT_COLOR, FONT_PATH)
        pygame.mouse.get_rel()
        mouse_timeout = 10
        sample_mouse = True
        
        while True:
            # Music Stuff
            utility.play_music(self.music_list)

            # Drawing Stuff
            self.screen.fill(FILL_COLOR)
            self.menu_group.update()
            self.menu_tooltip_group.update()
            self.cursor_group.update()
            try:
                self.screen.blit(self.background_image, self.background_image.get_rect())
            except:
                self.background_image.draw(self.screen)

            self.menu_group.draw(self.screen)
            self.menu_tooltip_pointer[self.current_selection].draw(self.screen)
            self.cursor_group.draw(self.screen)

            pygame.display.flip()

            self.cursor.position = vector.Vector2d(pygame.mouse.get_pos()) + vector.Vector2d(32, 32)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    utility.play_sound(self.menu_forward_sound)

                    return self.menu_dictionary.keys()[self.current_selection]

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    utility.play_sound(self.menu_forward_sound)

                    return self.menu_dictionary.keys()[self.current_selection]

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    utility.play_sound(self.menu_back_sound)

                    return False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    utility.play_sound(self.menu_back_sound)

                    return False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.menu_selection_pointer[self.current_selection].set_font(32, FONT_INACTIVE_COLOR, FONT_PATH)
                    self.current_selection -= 1

                    if self.current_selection < 0:
                        self.current_selection = len(self.menu_dictionary) - 1

                    self.menu_selection_pointer[self.current_selection].set_font(48, FONT_COLOR, FONT_PATH)
                    utility.play_sound(self.menu_beep_sound)

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.menu_selection_pointer[self.current_selection].set_font(32, FONT_INACTIVE_COLOR, FONT_PATH)
                    self.current_selection += 1

                    if self.current_selection > len(self.menu_dictionary) - 1:
                        self.current_selection = 0

                    self.menu_selection_pointer[self.current_selection].set_font(48, FONT_COLOR, FONT_PATH)
                    utility.play_sound(self.menu_beep_sound)

                elif event.type == pygame.MOUSEMOTION:
                    for element in self.menu_group:
                        if element.mouse_over():
                            if element.text_index != self.current_selection:
                                self.menu_selection_pointer[self.current_selection].set_font(32, FONT_INACTIVE_COLOR, FONT_PATH)
                                mouse_selection = element.text_index
                                self.current_selection = mouse_selection
                                self.menu_selection_pointer[self.current_selection].set_font(48, FONT_COLOR, FONT_PATH)
                                utility.play_sound(self.menu_beep_sound)

                """
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    for element in self.menuTooltipGroup:
                        print 'ELEMENT: ', element.text_index
                        element.mouseOverDump()

                elif event.type == pygame.MOUSEMOTION:
                    mouseInput = list(pygame.mouse.get_rel())
                    if sample_mouse:
                        if mouseInput[1] < -10:
                            self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                            self.currentSelection -= 1
                            if self.currentSelection < 0:
                                self.currentSelection = len(self.menuDictionary) - 1
                            self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                            sample_mouse = False
                            utility.playSound(self.menuBeep)

                        elif mouseInput[1] > 10:
                            self.menuSelectionPointer[self.currentSelection].setFont(32, FONT_INACTIVE_COLOR, FONT_PATH)
                            self.currentSelection += 1
                            if self.currentSelection > len(self.menuDictionary) - 1:
                                self.currentSelection = 0
                            self.menuSelectionPointer[self.currentSelection].setFont(48, FONT_COLOR, FONT_PATH)
                            sample_mouse = False
                            utility.playSound(self.menuBeep)   
                """

            if not sample_mouse:
                mouse_timeout -= 1
                
            if mouse_timeout == 0:
                sample_mouse = True
                mouse_timeout = 3
                
            self.timer.tick(30)
                
                
class Cursor(actor.Actor):
    master_animation_list = animation.Animation()

    def __init__(self):
        actor.Actor.__init__(self)
        
        self.animation_list = copy.copy(self.master_animation_list)
        self.animation_list.set_parent(self)
        self.animation_list.play('Idle')
        self.rect = self.image.get_rect()
        self.bound_style == BOUND_STYLE_CLAMP
        self.bounds = 32, 32, SCREEN_WIDTH, SCREEN_HEIGHT
        self.position = vector.Vector2d.zero
        self.velocity = vector.Vector2d.zero
        
    def mouse_over(self):
        pass