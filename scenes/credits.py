import scene
from ui import text
from utils import utility
from utils.utility import *


class Credits(object):
    def __init__(self, screen, music_list):
        self.music_list = music_list
        self.screen = screen
        self.new_scene = scene.ForestScene()
        self.finished = False
        self.scroll_rate = -1
        self.rolling_credits = True
        self.roll_credits()

    def roll_credits(self):
        credit_group = pygame.sprite.Group()

        # Create Text Labels
        title_credit = text.Text(FONT_PATH, 48, FONT_COLOR, 'Credits')
        title_credit.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT))

        big_jony = text.Text(FONT_PATH, 36, FONT_COLOR, 'Jony Fries')
        big_jony.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 100))
        jony_credit0 = text.Text(FONT_PATH, 24, FONT_COLOR, 'Game Programming')
        jony_credit0.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 150))
        jony_credit1 = text.Text(FONT_PATH, 24, FONT_COLOR, 'Sound Design')
        jony_credit1.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200))
        jony_credit2 = text.Text(FONT_PATH, 24, FONT_COLOR, 'Voice Acting')
        jony_credit2.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 250))

        big_josh = text.Text(FONT_PATH, 36, FONT_COLOR, 'Joshua Skelton')
        big_josh.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 350))
        josh_credit0 = text.Text(FONT_PATH, 24, FONT_COLOR, 'Game Programming')
        josh_credit0.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 400))
        josh_credit1 = text.Text(FONT_PATH, 24, FONT_COLOR, ' Graphic Design')
        josh_credit1.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 450))
        
        big_special = text.Text(FONT_PATH, 36, FONT_COLOR, 'Special Thanks To:')
        big_special.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 550))
        special_credit0 = text.Text(FONT_PATH, 24, FONT_COLOR, 'Python Software Foundation')
        special_credit0.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 600))
        special_credit1 = text.Text(FONT_PATH, 24, FONT_COLOR, 'PyGame')
        special_credit1.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 650))
        special_credit2 = text.Text(FONT_PATH, 24, FONT_COLOR, 'ShyFonts Type Foundry')
        special_credit2.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 700))
        
        thank_you = text.Text(FONT_PATH, 64, FONT_COLOR, 'Thank You For Playing!')
        thank_you.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 800))

        # Add Labels to Group
        credit_group.add(title_credit)
        
        credit_group.add(big_jony)
        credit_group.add(jony_credit0)
        credit_group.add(jony_credit1)
        credit_group.add(jony_credit2)
        
        credit_group.add(big_josh)
        credit_group.add(josh_credit0)
        credit_group.add(josh_credit1)
        
        credit_group.add(big_special)
        credit_group.add(special_credit0)
        credit_group.add(special_credit1)
        credit_group.add(special_credit2)

        credit_group.add(thank_you)

        timer = 5 * FRAMES_PER_SECOND

        for credit in credit_group:
            credit.set_alignment(CENTER_MIDDLE)

        while self.rolling_credits:
            utility.play_music(self.music_list)

            for credit in credit_group:
                credit_position = credit.get_position()
                credit.set_position((credit_position[0], credit_position[1] + self.scroll_rate))

            credit_group.update()
            self.new_scene.draw(self.screen)
            credit_group.draw(self.screen)
            pygame.display.flip()
            self.handle_events()
            
            if special_credit2.get_position()[1] < 0:
                if self.finished:
                    self.rolling_credits = False

            if thank_you.get_position()[1] < (SCREEN_HEIGHT / 2):
                thank_you.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN):
                self.scroll_rate = -10
                self.finished = True
