import pygame

from scenes import scenery
from utils import aitools
from utils.settings import *


class RockyScene(object):
    def __init__(self):
        self.actor_group1 = pygame.sprite.Group()
        self.actor_group2 = pygame.sprite.Group()
        self.actor_group3 = pygame.sprite.Group()
        self.cloud_timer = 0
        scenery.load_data()
        self.do_once = True
        self.screen = None

    def render(self):
        self.actor_group3.draw(self.screen)
        self.actor_group2.draw(self.screen)
        self.actor_group1.draw(self.screen)

    def update(self):
        if self.do_once:
            clouds_to_create = 11

            while clouds_to_create:
                temp_cloud = scenery.CloudSmall()
                aitools.spawn_on_screen(temp_cloud)
                self.actor_group2.add(temp_cloud)
                clouds_to_create -= 1
                
            islands_to_create = 3
            while islands_to_create:
                temp_island = scenery.IslandBig()
                aitools.spawn_on_screen(temp_island)
                self.actor_group2.add(temp_island)
                islands_to_create -= 1
                
            clouds_to_create = 7

            while clouds_to_create:
                temp_cloud = scenery.Cloud()
                aitools.spawn_on_screen(temp_cloud)
                self.actor_group1.add(temp_cloud)
                clouds_to_create -= 1

            self.do_once = False
            
            islands_to_create = 9

            while islands_to_create:
                temp_island = scenery.IslandSmall()
                aitools.spawn_on_screen(temp_island)
                self.actor_group3.add(temp_island)
                islands_to_create -= 1
        
        self.actor_group3.update()
        self.actor_group2.update()
        self.actor_group1.update()

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(FILL_COLOR)
        self.update()
        self.render()


class ForestScene(object):
    def __init__(self):
        self.actor_group1 = pygame.sprite.Group()
        self.actor_group2 = pygame.sprite.Group()
        self.actor_group3 = pygame.sprite.Group()
        self.cloud_timer = 0
        scenery.load_data()
        self.do_once = True
        self.screen = None

    def render(self):
        self.actor_group3.draw(self.screen)
        self.actor_group2.draw(self.screen)
        self.actor_group1.draw(self.screen)

    def update(self):
        if self.do_once:
            clouds_to_create = 3

            while clouds_to_create:
                temp_island = scenery.WhiteCloud()
                aitools.spawn_on_screen(temp_island)
                self.actor_group1.add(temp_island)
                clouds_to_create -= 1
                
            trees_to_create = 3

            while trees_to_create:
                temp_tree = scenery.TreeBig()
                aitools.spawn_on_screen(temp_tree)
                self.actor_group1.add(temp_tree)
                trees_to_create -= 1
                
            clouds_to_create = 4

            while clouds_to_create:
                temp_island = scenery.WhiteCloudSmall()
                aitools.spawn_on_screen(temp_island)
                self.actor_group2.add(temp_island)
                clouds_to_create -= 1

            trees_to_create = 4

            while trees_to_create:
                temp_tree = scenery.TreeSmall()
                aitools.spawn_on_screen(temp_tree)
                self.actor_group2.add(temp_tree)
                trees_to_create -= 1
                
            clouds_to_create = 6

            while clouds_to_create:
                temp_island = scenery.WhiteCloudTiny()
                aitools.spawn_on_screen(temp_island)
                self.actor_group3.add(temp_island)
                clouds_to_create -= 1

            self.do_once = False

        self.actor_group3.update()
        self.actor_group2.update()
        self.actor_group1.update()

    def draw(self, screen):
        self.screen = screen
        self.screen.fill((200, 200, 234))
        self.update()
        self.render()
        

class PinkScene(object):
    def __init__(self):
        self.actor_group1 = pygame.sprite.Group()
        self.actor_group2 = pygame.sprite.Group()
        self.actor_group3 = pygame.sprite.Group()
        scenery.load_data()
        self.do_once = True
        self.screen = None

    def render(self):
        self.actor_group3.draw(self.screen)
        self.actor_group2.draw(self.screen)
        self.actor_group1.draw(self.screen)

    def update(self):
        if self.do_once:
            clouds_to_create = 6

            while clouds_to_create:
                temp_cloud = scenery.BlueCloud()
                aitools.spawn_on_screen(temp_cloud)
                self.actor_group1.add(temp_cloud)
                clouds_to_create -= 1
                
            clouds_to_create = 6

            while clouds_to_create:
                temp_cloud = scenery.BlueCloudSmall()
                aitools.spawn_on_screen(temp_cloud)
                self.actor_group2.add(temp_cloud)
                clouds_to_create -= 1
                
            stars_to_create = 12

            while stars_to_create:
                temp_star = scenery.SmallStar()
                aitools.spawn_on_screen(temp_star)
                self.actor_group3.add(temp_star)
                stars_to_create -= 1

            self.do_once = False
          
        self.actor_group1.update()
        self.actor_group2.update()
        self.actor_group3.update()

    def draw(self, screen):
        self.screen = screen
        self.screen.fill((234, 203, 200))
        self.update()
        self.render()


class TutorialScene(object):
    def __init__(self):
        self.actor_group1 = pygame.sprite.Group()
        scenery.load_data()
        self.do_once = True
        self.screen = None

    def render(self):
        self.actor_group1.draw(self.screen)

    def update(self):
        if self.do_once:
            self.do_once = False
          
        self.actor_group1.update()

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(FILL_COLOR)
        self.update()
        self.render()
