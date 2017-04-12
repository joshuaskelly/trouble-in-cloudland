import player
import world
from scenes import credits, scene, tutorial
from ui import icon, menu, text
from utils import prettyprint, utility, vector
from utils.utility import *

pause_menu_dictionary = {
    RESUME_GAME: ['Resume','Continue Playing'],
    OPTION_MENU: ['Options','Change Sound and Video Options'],
    EXIT_GAME: ['Exit','Exit to the Main Menu']
}


class Game(object):
    def __init__(self, screen, world_to_start, music_list):
        self.screen = screen

        pygame.mouse.set_visible(False)

        self.done = False
        self.world_done = False

        self.high_score = 0

        self.bullet_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.Group()
        self.effects_group = pygame.sprite.Group()
        
        self.mouse_last_move = MOUSE_DEFAULT_POSITION

        self.group_list = [
            self.powerup_group,
            self.enemy_group,
            self.boss_group,
            self.text_group,
            self.effects_group
        ]

        self.score_board = text.Text(FONT_PATH, 36, FONT_COLOR)
        self.temp_life_board = text.Text(FONT_PATH, 36, FONT_COLOR)
        self.temp_life_board.position = vector.Vector2d(48, 40)
        self.life_board = self.temp_life_board
        
        self.life_icon = icon.Icon('life')
        
        self.player = player.Player(self.bullet_group, self.effects_group, self.life_board, self.score_board)
        
        self.player_group.add(self.player)
        self.text_group.add(self.score_board)
        self.text_group.add(self.temp_life_board)
        self.text_group.add(self.life_icon)

        self.music_list = music_list

        self.timer = pygame.time.Clock()

        # Get rid of the first mouse delta
        pygame.mouse.get_rel()

        world1_level0 = [
            [0, ACTOR_MOONO, 45, 0],
            [1, ACTOR_MOONO, 120, 0],
            [2, ACTOR_MOONO, 240, 0],
            [3, ACTOR_BAAKE, -1 ,1],
            [4, ACTOR_BOSS_TUT, -1, 1],
            [4, ACTOR_MOONO, 35, 0]
        ]

        world1_level1 = [
            [0, ACTOR_MOONO, 40, 0],
            [1, ACTOR_MOONO, 85, 0],
            [2, ACTOR_MOONO, 110, 0],
            [3, ACTOR_BAAKE, -1 ,2],
            [4, ACTOR_BOSS_TUT, -1, 1],
            [4, ACTOR_MOONO, 30, 0]
        ]

        world1_level2 = [
            [0, ACTOR_MOONO, 30, 0],
            [1, ACTOR_BAAKE, -1, 1],
            [0, ACTOR_MOONO, 70, 0],
            [2, ACTOR_BAAKE, -1, 1],
            [0, ACTOR_MOONO, 130, 0],
            [3, ACTOR_BAAKE, -1, 1],
            [0, ACTOR_MOONO, 300, 0],
            [4, ACTOR_BOSS_TUT, -1, 1],
            [4, ACTOR_MOONO, 25, 0]
        ]

        world1_level3 = [
            [0, ACTOR_MOONO, 25, 0],
            [1, ACTOR_BAAKE, -1, 1],
            [1, ACTOR_MOONO, 50, 0],
            [2, ACTOR_BAAKE, -1, 2],
            [2, ACTOR_MOONO, 110, 0],
            [3, ACTOR_BAAKE, -1, 2],
            [3, ACTOR_MOONO, 210, 0],
            [4, ACTOR_BOSS_TUT, -1, 1],
            [4, ACTOR_MOONO, 20, 0]
        ]

        world2_level0 = [
            [0, ACTOR_MOONO, 45, 0],
            [0, ACTOR_HAOYA, 65, 0],
            [1, ACTOR_BAAKE, -1, 1],
            [1, ACTOR_MOONO, 70, 0],
            [2, ACTOR_HAOYA, 75, 0],
            [3, ACTOR_MOONO, 85, 0],
            [4, ACTOR_BAAKE_BOSS, -1, 1],
            [4, ACTOR_HAOYA, 30, 0]
        ]

        world2_level1 = [
            [0, ACTOR_BAAKE, -1, 2],
            [0, ACTOR_BATTO, 150 ,0],
            [0, ACTOR_MOONO, 55, 0],
            [1, ACTOR_HAOYA, 60, 0],
            [2, ACTOR_MOONO, 100 ,0],
            [3, ACTOR_BAAKE, -1, 1],
            [3, ACTOR_BATTO, 280, 0],
            [4, ACTOR_BAAKE_BOSS, -1, 1],
            [4, ACTOR_BATTO, 70, 0]
        ]

        world2_level2 = [
            [0, ACTOR_ROKUBI, 60, 0],
            [0, ACTOR_MOONO, 50, 0],
            [0, ACTOR_BAAKE, -1, 2],
            [1, ACTOR_BAAKE, -1, 1],
            [1, ACTOR_BATTO, 160, 0],
            [2, ACTOR_HAOYA, 60, 0],
            [3, ACTOR_MOONO, 80, 0],
            [4, ACTOR_BAAKE_BOSS, -1, 1],
            [4, ACTOR_ROKUBI, 30, 0]
        ]

        world2_level3 = [
            [0, ACTOR_HAOYA, 60, 0],
            [0, ACTOR_BATTO, 170, 0],
            [0, ACTOR_ROKUBI, 75, 0],
            [0, ACTOR_BAAKE, -1, 1],
            [1, ACTOR_MOONO, 70, 0],
            [1, ACTOR_BAAKE, -1, 1],
            [2, ACTOR_BAAKE, -1, 1],
            [2, ACTOR_ROKUBI, 180, 1],
            [3, ACTOR_MOONO, 200, 0],
            [4, ACTOR_BAAKE_BOSS, -1, 1],
            [4, ACTOR_HAOYA, 100, 0],
            [4, ACTOR_BATTO, 240, 0],
            [4, ACTOR_ROKUBI, 90, 0],
            [4, ACTOR_BAAKE, -1, 1]
        ]

        world3_level0 = [
            [0, ACTOR_HAKTA, 35, 0],
            [0, ACTOR_HAOYA, 65, 0],
            [1, ACTOR_BOKKO, -1, 1],
            [2, ACTOR_BOKKO, -1, 1],
            [2, ACTOR_HAKTA, 75, 0],
            [3, ACTOR_BOKKO, -1, 1],
            [4, ACTOR_MOONO_BOSS, -1, 1],
            [4, ACTOR_HAKTA, 30, 0]
        ]

        world3_level1 = [
            [0, ACTOR_RAAYU, 45, 0],
            [0, ACTOR_HAKTA, 50, 0],
            [1, ACTOR_BOKKO, -1, 1],
            [2, ACTOR_RAAYU, 60, 0],
            [3, ACTOR_BOKKO, -1, 1],
            [3, ACTOR_ROKUBI, 80, 0],
            [4, ACTOR_MOONO_BOSS, -1, 1],
            [4, ACTOR_RAAYU, 25, 0]
        ]

        world3_level2 = [
            [0, ACTOR_PAAJO, 95, 0],
            [0, ACTOR_HAKTA, 40, 0],
            [1, ACTOR_BOKKO, -1, 2],
            [2, ACTOR_RAAYU, 80, 0],
            [3, ACTOR_BOKKO, -1, 1],
            [4, ACTOR_MOONO_BOSS, -1, 1],
            [4, ACTOR_PAAJO, 70, 0]
        ]

        world3_level3 = [
            [0, ACTOR_HAKTA, 55, 0],
            [0, ACTOR_RAAYU, 75, 0],
            [0, ACTOR_PAAJO, 160, 0],
            [1, ACTOR_BOKKO, -1, 2],
            [1, ACTOR_ROKUBI, 50, 0],
            [2, ACTOR_HAOYA, 120, 0],
            [3, ACTOR_BOKKO, -1, 1],
            [4, ACTOR_MOONO_BOSS, -1, 1],
            [4, ACTOR_HAKTA, 60, 0],
            [4, ACTOR_RAAYU, 50, 0],
            [4, ACTOR_PAAJO, 110, 0],
            [4, ACTOR_BOKKO, -1, 1]
        ]
        
        tutorial_world = ['Tutorial', self.player, self.group_list]
        temp_world_1 = ['Cloudopolis', self.player, self.group_list, [world1_level0, world1_level1, world1_level2, world1_level3]]
        temp_world_2 = ['Nightmaria', self.player, self.group_list, [world2_level0, world2_level1, world2_level2, world2_level3]]
        temp_world_3 = ['Opulent Dream', self.player, self.group_list, [world3_level0, world3_level1, world3_level2, world3_level3]]

        self.world_list = [
            tutorial_world,
            temp_world_1,
            temp_world_2,
            temp_world_3
        ]

        self.world_number = world_to_start

        if self.world_number == 0:
            self.current_world = tutorial.Tutorial(self.world_list[self.world_number])

        else:
            self.current_world = world.World(self.world_list[self.world_number], self.music_list[self.world_number])
            self.current_world.load()

        if self.world_number == 0:
            self.new_scene = scene.TutorialScene()
            self.player.lives = 99
            self.life_board.set_text('x' + str(self.player.lives))

        elif self.world_number == 1:
            self.new_scene = scene.ForestScene()

        elif self.world_number == 2:
            self.new_scene = scene.RockyScene()

        elif self.world_number == 3:
            self.new_scene = scene.PinkScene()

    def run(self):
        while not self.done:
            if self.world_done:
                if self.world_number < MAX_WORLD:
                    self.world_beat()

                    # Resetting player lives so that it isn't in their best
                    # interest to play easier worlds just to have extra lives.
                    self.player.lives = 3
                    self.player.life_board.set_text('x' + str(self.player.lives))
                    
                    self.player.score = 0
                    self.player.next_bonus = 50000

                    # Loading the new world
                    self.world_number += 1
                    
                    if self.world_number == 0:
                        self.new_scene = scene.TutorialScene()

                    elif self.world_number == 1:
                        self.new_scene = scene.ForestScene()

                    elif self.world_number == 2:
                        self.new_scene = scene.RockyScene()

                    elif self.world_number == 3:
                        self.new_scene = scene.PinkScene()
                    
                    if self.world_number > settings_list[WORLD_UNLOCKED]:
                        settings_list[WORLD_UNLOCKED] = self.world_number

                    utility.play_music(self.music_list[self.world_number], True)
                    self.current_world = world.World(self.world_list[self.world_number], self.music_list[self.world_number])
                    self.current_world.load()
                    self.world_done = False
                        
                else:
                    self.game_beat()

            self.check_collision()
            self.update()
            self.draw()
            self.handle_events()
            
            pygame.mouse.set_pos(MOUSE_DEFAULT_POSITION)
            pygame.mouse.get_rel()
            self.mouse_last_move = pygame.mouse.get_pos()
            
            self.timer.tick(FRAMES_PER_SECOND)
     
            if self.player.dead:
                high_score = read_high_scores()

                if self.player.score < high_score[self.world_number]:
                    end_game_dictionary = {
                        HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You would need to score ' + str(high_score[self.world_number] - self.player.score) + ' more to beat it!'],
                        NEXT_WORLD: ['Exit', 'Return To The Menu']
                    }

                elif self.player.score == high_score[self.world_number]:
                    end_game_dictionary = {
                        HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Tied the High Score!'],
                        NEXT_WORLD: ['Exit', 'Return To The Menu']
                    }

                else:
                    end_game_dictionary = {
                        HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Beat the High Score!'],
                        NEXT_WORLD: ['Exit', 'Return To The Menu']
                    }

                    high_score[self.world_number] = self.player.score
                    write_high_scores(high_score)

                utility.dim(128, FILL_COLOR)

                end_game_menu = menu.Menu(self.screen,
                                          self.music_list[self.world_number],
                                          self.screen.convert(),
                                          [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                          ['Game Over', 128, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                          end_game_dictionary)

                end_game_menu.show()

                self.done = True
                utility.fade_music()
                utility.play_music(self.music_list[MENU_MUSIC], True)

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) or (event.type == pygame.ACTIVEEVENT and event.gain == 0):
                utility.dim(128, FILL_COLOR)

                # Grab a copy of the screen to show behind the menu
                screen_grab = self.screen.copy()
                pause_menu_running = True
                
                while pause_menu_running:
                    pause_menu = menu.Menu(self.screen,
                                           self.music_list[self.world_number],
                                           screen_grab,
                                           [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                           ['Pause', 128, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                           pause_menu_dictionary)

                    menu_result = pause_menu.show()
    
                    if menu_result == OPTION_MENU:
                        option_result = True
                        last_highlighted = 0

                        while option_result:
    
                            option_menu_dictionary = {
                                SOUND_MENU: ['Sound Options', 'Change Sound Options'],
                                DISPLAY_MENU: ['Video Options', 'Change Video Options'],
                                CHANGE_SENSITIVITY: ['Mouse Sensitivity: ' + prettyprint.mouse_sensitivity(settings_list[SENSITIVITY]), 'Change Mouse Sensitivity'],
                                EXIT_OPTIONS: ['Back', 'Go Back to the Main Menu']
                            }
    
                            sensitivity_menu_dictionary = {
                                0: ['Very Low', 'Change Sensitivity to Very Low'],
                                1: ['Low', 'Change Sensitivity to Low'],
                                2: ['Normal', 'Change Sensitivity to Normal'],
                                3: ['High', 'Change Sensitivity to High'],
                                4: ['Very High', 'Change Sensitivity to Very High']
                            }
                            
                            sound_menu_dictionary = {
                                TOGGLE_SFX: ['Sound Effects: ' + prettyprint.on(settings_list[SFX]), 'Turn ' + prettyprint.on(not settings_list[SFX]) + ' Sound Effects'],
                                TOGGLE_MUSIC: ['Music: ' + prettyprint.on(settings_list[MUSIC]), 'Turn ' + prettyprint.on(not settings_list[MUSIC]) + ' Music'],
                                EXIT_OPTIONS: ['Back', 'Go Back to the Option Menu']
                            }
                            
                            display_menu_dictionary = {
                                TOGGLE_PARTICLES: ['Particles: ' + prettyprint.able(settings_list[PARTICLES]), 'Turn ' + prettyprint.on(not settings_list[PARTICLES]) + ' Particle Effects'],
                                TOGGLE_FULLSCREEN: ['Video Mode: ' + prettyprint.screen_mode(settings_list[SETTING_FULLSCREEN]), 'Switch To ' + prettyprint.screen_mode(not settings_list[SETTING_FULLSCREEN]) + ' Mode'],
                                EXIT_OPTIONS: ['Back', 'Go Back to the Main Menu']
                            }
    
                            option_result = menu.Menu(self.screen,
                                                      self.music_list[self.world_number],
                                                      screen_grab,
                                                      [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                                      ['Options', 96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                                      option_menu_dictionary,
                                                      last_highlighted).show()
                            
                            if option_result == SOUND_MENU:
                                sound_result = True
                                last_highlighted = 0

                                while sound_result:
                                    sound_menu = menu.Menu(self.screen,
                                                           self.music_list[self.world_number],
                                                           screen_grab,
                                                           [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                                           ['Sound Options', 96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                                           sound_menu_dictionary,
                                                           last_highlighted)

                                    sound_result = sound_menu.show()
                                    
                                    if sound_result == TOGGLE_SFX:
                                        settings_list[SFX] = not settings_list[SFX]
                                        last_highlighted = 0
                                    
                                    elif sound_result == TOGGLE_MUSIC:
                                        settings_list[MUSIC] = not settings_list[MUSIC]

                                        if not settings_list[MUSIC]:
                                            pygame.mixer.Channel(MUSIC_CHANNEL).stop()

                                        last_highlighted = 1
                                        
                                    elif sound_result == EXIT_OPTIONS:
                                        sound_result = False
                                        
                                    sound_menu_dictionary = {
                                        TOGGLE_SFX: ['Sound Effects: ' + prettyprint.on(settings_list[SFX]), 'Turn ' + prettyprint.on(not settings_list[SFX]) + ' Sound Effects'],
                                        TOGGLE_MUSIC: ['Music: ' + prettyprint.on(settings_list[MUSIC]), 'Turn ' + prettyprint.on(not settings_list[MUSIC]) + ' Music'],
                                        EXIT_OPTIONS: ['Back', 'Go Back to the Option Menu']
                                    }
                                        
                            if option_result == DISPLAY_MENU:
                                display_result = True
                                last_highlighted = 0

                                while display_result:
                                    
                                    display_menu = menu.Menu(self.screen,
                                                             self.music_list[self.world_number],
                                                             screen_grab,
                                                             [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                                             ['Video Options', 96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                                             display_menu_dictionary,
                                                             last_highlighted)

                                    display_result = display_menu.show()
                            
                                    if display_result == TOGGLE_PARTICLES:
                                        settings_list[PARTICLES] = not settings_list[PARTICLES]
                                        last_highlighted = 0
                                        
                                    elif display_result == TOGGLE_FULLSCREEN:
                                        settings_list[SETTING_FULLSCREEN] = not settings_list[SETTING_FULLSCREEN]
                                        last_highlighted = 1
                                        pygame.mixer.quit()
                                        pygame.mixer.init()
                                        
                                        if settings_list[SETTING_FULLSCREEN]:
                                            utility.set_fullscreen()
                                        else:
                                            utility.set_fullscreen(False)
                                            
                                        pygame.mouse.set_visible(False)
                                        
                                    elif display_result == EXIT_OPTIONS:
                                        display_result = False
                                        
                                    display_menu_dictionary = {
                                        TOGGLE_PARTICLES: ['Particles: ' + prettyprint.able(settings_list[PARTICLES]), 'Turn ' + prettyprint.on(not settings_list[PARTICLES]) + ' Particle Effects'],
                                        TOGGLE_FULLSCREEN: ['Video Mode: ' + prettyprint.screen_mode(settings_list[SETTING_FULLSCREEN]), 'Switch To ' + prettyprint.screen_mode(not settings_list[SETTING_FULLSCREEN]) + ' Mode'],
                                        EXIT_OPTIONS: ['Back', 'Go Back to the Main Menu']
                                    }
                            
                            elif option_result == EXIT_OPTIONS:
                                option_result = False
                            
                            elif option_result == CHANGE_SENSITIVITY:
                                sensitivity_result = True
                                last_highlighted = 0

                                while sensitivity_result:
                                    sensitivity_menu = menu.Menu(self.screen,
                                                                 self.music_list[self.world_number],
                                                                 screen_grab,
                                                                 [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                                                 ['Mouse Sensitivity', 96,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                                                 sensitivity_menu_dictionary,
                                                                 last_highlighted)

                                    sensitivity_result = sensitivity_menu.show()
                                    mouse_sensitivities = [0.5, 0.75, 1, 1.25, 1.5]
                                    settings_list[SENSITIVITY] = mouse_sensitivities[sensitivity_result]

                                    if sensitivity_result > 0:
                                        sensitivity_result = False
                                
                    elif menu_result == RESUME_GAME or menu_result == False:
                        pause_menu_running = False
                        pygame.mouse.get_rel()
    
                    elif menu_result == EXIT_GAME:
                        utility.fade_music()
                        utility.play_music(self.music_list[MENU_MUSIC], True)
                        self.done = True
                        pause_menu_running = False
                                       
            elif event.type == pygame.MOUSEMOTION and self.player.lives:
                mouse_input = [pygame.mouse.get_pos()[0] - 512.0, pygame.mouse.get_pos()[1] - 384.0]

                if mouse_input[0] != 0 and mouse_input[1] != 0:
                    self.player.fire()
                    self.player.velocity = (self.player.velocity + mouse_input) / 1.5 * settings_list[SENSITIVITY]
                    
    def draw(self):
        self.screen.fill(FILL_COLOR)
        self.new_scene.draw(self.screen)
        self.effects_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.powerup_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.boss_group.draw(self.screen)
        self.text_group.draw(self.screen)
        
        pygame.display.flip()

    def update(self):
        self.world_done = self.current_world.update()
        self.enemy_group.update()
        self.player_group.update()
        self.bullet_group.update()
        self.powerup_group.update()
        self.boss_group.update()
        self.text_group.update()
        self.effects_group.update()

    def check_collision(self):
        if self.player.active:
            self.player.check_collision(self.powerup_group)
            self.player.check_collision(self.enemy_group)
            self.player.check_collision(self.boss_group)

        for boss in self.boss_group:
            if boss.active:
                boss.check_collision(self.bullet_group)

        for enemy in self.enemy_group:
            if enemy.active:
                enemy.check_collision(self.powerup_group)
                enemy.check_collision(self.bullet_group)

    def world_beat(self):
        high_score = read_high_scores()

        if self.player.score < high_score[self.world_number]:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You would need to score ' + str(high_score[self.world_number] - self.player.score) + ' more to beat it!'],
                NEXT_WORLD: ['Continue', 'On to the Next World!']
            }

        elif self.player.score == high_score[self.world_number]:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Tied the High Score!'],
                NEXT_WORLD: ['Continue', 'On to the Next World!']
            }

        else:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Beat the High Score!'],
                NEXT_WORLD: ['Continue', 'On to the Next World!']
            }

            high_score[self.world_number] = self.player.score
            write_high_scores(high_score)

        utility.dim(128, FILL_COLOR)

        # Show world defeated menu
        menu.Menu(self.screen,
                  self.music_list[self.world_number],
                  self.screen.convert(),
                  [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                  ['World Defeated!', 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                  world_end_dictionary).show()
         
        utility.fade_music()

    def game_beat(self):
        high_score = read_high_scores()

        if self.player.score < high_score[self.world_number]:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You would need to score ' + str(high_score[self.world_number] - self.player.score) + ' more to beat it!'],
                NEXT_WORLD: ['Credits', 'On to the Credits!']
            }

        elif self.player.score == high_score[self.world_number]:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Tied the High Score!'],
                NEXT_WORLD: ['Credits', 'On to the Credits!']
            }

        else:
            world_end_dictionary = {
                HIGH_SCORE: ['High Score For This World: ' + str(high_score[self.world_number]), 'You Beat the High Score!'],
                NEXT_WORLD: ['Credits', 'On to the Credits!']
            }

            high_score[self.world_number] = self.player.score
            write_high_scores(high_score)

        utility.dim(128, FILL_COLOR)

        world_end_menu = menu.Menu(self.screen,
                                   self.music_list[self.world_number],
                                   self.screen.convert(),
                                   [0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT],
                                   ['Congratulations!', 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
                                   world_end_dictionary)

        world_end_menu.show()

        utility.fade_music()
        credits.Credits(self.screen, self.music_list[MENU_MUSIC])
        
        self.done = True
