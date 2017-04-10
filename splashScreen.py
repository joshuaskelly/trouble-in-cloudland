import icon
import pygame
import utility

from settings import *

class SplashScreen:
    def __init__(self, screen, image, fadeImage = True, music = None):
        self.image = icon.Icon(image)
        self.fadeImage = fadeImage
        self.screen = screen
        self.music = music
        self.clock = pygame.time.Clock()
        
        self.displayScreen()
    
    def displayScreen(self):
        self.timer = 4.0 * FRAMES_PER_SECOND
        sequence = 1 * FRAMES_PER_SECOND

        while self.timer:
            self.handleEvents()

            self.screen.fill(FILL_COLOR)
            if self.music:
                utility.play_music(self.music)
            self.timer -= 1
            
            self.image.draw(self.screen)
            
            if self.timer >= 3 * FRAMES_PER_SECOND:
                utility.dim((sequence / (1.0 * FRAMES_PER_SECOND)) * 255)
                sequence -= 1
            if self.timer <= 1 * FRAMES_PER_SECOND:
                if self.fadeImage:
                    utility.dim((sequence / (1.0 * FRAMES_PER_SECOND)) * 255)
                sequence += 1
                
            pygame.display.flip()

            self.clock.tick(FRAMES_PER_SECOND)
    
    def handleEvents(self):
        for event in pygame.event.get():
            if self.timer > FRAMES_PER_SECOND:
                if event.type == pygame.KEYDOWN:
                    self.timer = FRAMES_PER_SECOND + 1
            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.timer = FRAMES_PER_SECOND + 1                