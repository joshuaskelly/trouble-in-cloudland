import text
import scene
import utility

from utility import *
from pygame.locals import *

class Credits:
    def __init__(self,screen,musicList):
        self.musicList = musicList
        self.screen = screen
        self.newScene = scene.forestScene()
        self.finished = False
        self.scrollRate = -1

        self.rollCredits()

    
    def rollCredits(self):
        creditGroup = pygame.sprite.Group()

        """    Create Text Labels    """
        titleCredit  = text.Text(FONT_PATH,48,FONT_COLOR,"Credits")
        titleCredit.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT))

        bigJony   = text.Text(FONT_PATH,36,FONT_COLOR,"Jony Fries")
        bigJony.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 100))
        jonyCredit0  = text.Text(FONT_PATH,24,FONT_COLOR,"Game Programming")
        jonyCredit0.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 150))
        jonyCredit1  = text.Text(FONT_PATH,24,FONT_COLOR,"Sound Design")
        jonyCredit1.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 200))
        jonyCredit2  = text.Text(FONT_PATH,24,FONT_COLOR,"Voice Acting")
        jonyCredit2.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 250))

        bigJosh  = text.Text(FONT_PATH,36,FONT_COLOR,"Joshua Skelton")
        bigJosh.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 350))
        joshCredit0  = text.Text(FONT_PATH,24,FONT_COLOR,"Game Programming")
        joshCredit0.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 400))
        joshCredit1  = text.Text(FONT_PATH,24,FONT_COLOR,"Graphic Design")
        joshCredit1.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 450))
        
        bigSpecial = text.Text(FONT_PATH,36,FONT_COLOR,"Special Thanks To:")
        bigSpecial.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 550))
        specialCredit0 = text.Text(FONT_PATH,24,FONT_COLOR,"Python Software Foundation")
        specialCredit0.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 600))
        specialCredit1 = text.Text(FONT_PATH,24,FONT_COLOR,"PyGame")
        specialCredit1.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 650))
        specialCredit2 = text.Text(FONT_PATH,24,FONT_COLOR,"ShyFonts Type Foundry")
        specialCredit2.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 700))
        
        thankYou = text.Text(FONT_PATH,64,FONT_COLOR,"Thank You For Playing!")
        thankYou.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT + 800))

        """    Add Labels to Group    """
        creditGroup.add(titleCredit)
        
        creditGroup.add(bigJony)
        creditGroup.add(jonyCredit0)
        creditGroup.add(jonyCredit1)
        creditGroup.add(jonyCredit2)
        
        creditGroup.add(bigJosh)
        creditGroup.add(joshCredit0)
        creditGroup.add(joshCredit1)
        
        creditGroup.add(bigSpecial)
        creditGroup.add(specialCredit0)
        creditGroup.add(specialCredit1)
        creditGroup.add(specialCredit2)

        creditGroup.add(thankYou)

        self.rollingCredits = True
        timer = 5 * FRAMES_PER_SECOND

        for credit in creditGroup:
            credit.set_alignment(CENTER_MIDDLE)

        while self.rollingCredits:
            utility.play_music(self.musicList)
            for credit in creditGroup:
                creditPosition = credit.getPosition()
                credit.setPosition((creditPosition[0],creditPosition[1] + self.scrollRate))

            creditGroup.update()
            self.newScene.draw(self.screen)
            creditGroup.draw(self.screen)
            pygame.display.flip()
            self.handleEvents()
            
            if specialCredit2.getPosition()[1] < 0:
                if self.finished:
                    self.rollingCredits = False

            if thankYou.getPosition()[1] < (SCREEN_HEIGHT / 2):
                thankYou.setPosition((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


    def handleEvents(self):
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN):
                self.scrollRate = -10
                self.finished = True
                    