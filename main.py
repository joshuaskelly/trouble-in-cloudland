#!/usr/bin/python
import pygame

import balloon
import bullet
import credits
import enemies
import game
import gem
import menu
import particle
import player
import prettyprint
import scene
import splashscreen
import text
import utility
import vector
import world
from settings import *

pygame.init()

utility.read_settings()

if settings_list[SETTING_FULLSCREEN]:
    screen = utility.set_fullscreen()

else:
    screen = utility.set_fullscreen(False)
    
pygame.display.set_icon(utility.load_image('icon'))
pygame.display.set_caption('Trouble In CloudLand v1.1')

screen.fill((0, 0, 0))
tempText = text.Text(FONT_PATH, 36, (255, 255, 255))
tempText.set_text('Loading...')
tempText.position = vector.Vector2d((SCREEN_WIDTH / 2) - (tempText.image.get_width() / 2), (SCREEN_HEIGHT / 2) - (tempText.image.get_height() / 2))
tempText.update()
tempText.draw(screen)
pygame.display.flip()

try:
    pygame.mixer.set_reserved(MUSIC_CHANNEL)
    pygame.mixer.Channel(MUSIC_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(PLAYER_CHANNEL)
    pygame.mixer.Channel(PLAYER_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(OW_CHANNEL)
    pygame.mixer.Channel(OW_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(BAAKE_CHANNEL)
    pygame.mixer.Channel(BAAKE_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(BOSS_CHANNEL)
    pygame.mixer.Channel(BOSS_CHANNEL).set_volume(1)
    
    pygame.mixer.set_reserved(PICKUP_CHANNEL)
    pygame.mixer.Channel(PICKUP_CHANNEL).set_volume(1)

except:
    utility.sound_active = False
    print 'WARNING! - Sound not initialized.'

pygame.mouse.set_visible(False)
music_list = [
    utility.load_sound('menuMusic'),
    utility.load_sound('music0'),
    utility.load_sound('music1'),
    utility.load_sound('music2'),
    utility.load_sound('bossMusic')
]

world.load_data()
player.load_data()
bullet.load_data()
pygame.event.pump()
enemies.baake.load_data()
balloon.load_data()
gem.load_data()
pygame.event.pump()
enemies.moono.load_data()
enemies.batto.load_data()
enemies.rokubi.load_data()
pygame.event.pump()
enemies.haoya.load_data()
enemies.yurei.load_data()
enemies.bokko.load_data()
pygame.event.pump()
enemies.hakta.load_data()
enemies.raayu.load_data()
enemies.paajo.load_data()
pygame.event.pump()
enemies.boss.load_data()
particle.load_data()
menu.load_data()

for event in pygame.event.get():
    pass

splashscreen.SplashScreen(screen, 'pygamesplash')
utility.play_music(music_list[MENU_MUSIC])
splashscreen.SplashScreen(screen, 'gameSplash')

if settings_list[WORLD_UNLOCKED] == 0:
    new_scene = scene.TutorialScene()

elif settings_list[WORLD_UNLOCKED] == 1:
    new_scene = scene.ForestScene()

elif settings_list[WORLD_UNLOCKED] == 2:
    new_scene = scene.RockyScene()

elif settings_list[WORLD_UNLOCKED] == 3:
    new_scene = scene.PinkScene()

game_is_running = True

main_menu_dictionary = {
    START_GAME: ('Play', 'Start a New Game'),
    OPTION_MENU: ('Options', 'Change Sound and Video Options'),
    CREDIT_MENU: ('Credits', 'Who We Are, What We Did'),
    EXIT_GAME: ('Exit', 'Exit the Game')
}

world_menu_dictionary = {
    TUTORIAL: ('Tutorial', 'Start the Tutorial [Learn]'),
    WORLD1: ('Cloudopolis', 'Start Playing Cloudopolis [Apprentice]'),
    WORLD2: ('Nightmaria', 'Start Playing Nightmaria [Journeyman]'),
    WORLD3: ('Opulent Dream', 'Start Playing Opulent Dream [Master]'),
    EXIT_OPTIONS: ('Back', 'Go Back to the Main Menu')
}

option_menu_dictionary = {
    SOUND_MENU: ('Sound Options', 'Change Sound Options'),
    DISPLAY_MENU: ('Video Options', 'Change Video Options'),
    CHANGE_SENSITIVITY: ('Mouse Sensitivity: ' + prettyprint.mouse_sensitivity(settings_list[SENSITIVITY]), 'Change Mouse Sensitivity'),
    EXIT_OPTIONS: ('Back', 'Go Back to the Main Menu')
}

sound_menu_dictionary = {
    TOGGLE_SFX: ('Sound Effects: ' + prettyprint.on(settings_list[SFX]), 'Turn ' + prettyprint.on(not settings_list[SFX]) + ' Sound Effects'),
    TOGGLE_MUSIC: ('Music: ' + prettyprint.on(settings_list[MUSIC]), 'Turn ' + prettyprint.on(not settings_list[MUSIC]) + ' Music'),
    EXIT_OPTIONS: ('Back', 'Go Back to the Option Menu')
}

display_menu_dictionary = {
    TOGGLE_PARTICLES: ('Particles: ' + prettyprint.able(settings_list[PARTICLES]), 'Turn ' + prettyprint.on(not settings_list[PARTICLES]) + ' Particle Effects'),
    TOGGLE_FULLSCREEN: ('Video Mode: ' + prettyprint.screen_mode(settings_list[SETTING_FULLSCREEN]), 'Switch To ' + prettyprint.screen_mode(not settings_list[SETTING_FULLSCREEN]) + ' Mode'),
    EXIT_OPTIONS: ('Back', 'Go Back to the Main Menu')
}

sensitivity_menu_dictionary = {
    0: ('Very Low', 'Change Sensitivity to Very Low'),
    1: ('Low', 'Change Sensitivity to Low'),
    2: ('Normal', 'Change Sensitivity to Normal'),
    3: ('High', 'Change Sensitivity to High'),
    4: ('Very High', 'Change Sensitivity to Very High')
}

menu_bounds = (0, SCREEN_HEIGHT / 3, SCREEN_WIDTH, SCREEN_HEIGHT)

while game_is_running:
    menu_result = menu.Menu(screen,
                            music_list[MENU_MUSIC],
                            new_scene,
                            menu_bounds,
                            ('Trouble in Cloudland', 80, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                            main_menu_dictionary).show()

    if menu_result == START_GAME:
        last_highlighted = settings_list[WORLD_UNLOCKED]
        world_result = menu.Menu(screen,
                                 music_list[MENU_MUSIC],
                                 new_scene,
                                 menu_bounds,
                                 ('Choose a World', 96, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                                 world_menu_dictionary,
                                 last_highlighted).show()

        if world_result == TUTORIAL:
            game.Game(screen, 0, music_list).run()

        elif world_result == EXIT_OPTIONS:
            world_result = False

        elif world_result is not False:
            utility.fade_music()
            utility.play_music(music_list[world_result - 1], True)
            game.Game(screen, world_result - 1, music_list).run()

    elif menu_result == OPTION_MENU:
        option_result = True
        last_highlighted = 0
        while option_result:
            option_result = menu.Menu(screen,
                                      music_list[MENU_MUSIC],
                                      new_scene,
                                      menu_bounds,
                                      ('Options', 96, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                                      option_menu_dictionary,
                                      last_highlighted).show()
            
            if option_result == SOUND_MENU:
                sound_result = True
                last_highlighted = 0

                while sound_result:
                    sound_result = menu.Menu(screen,
                                             music_list[MENU_MUSIC],
                                             new_scene,
                                             menu_bounds,
                                             ('Sound Options', 96, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                                             sound_menu_dictionary,
                                             last_highlighted).show()
                    
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
                        TOGGLE_SFX: ('Sound Effects: ' + prettyprint.on(settings_list[SFX]), 'Turn ' + prettyprint.on(not settings_list[SFX]) + ' Sound Effects'),
                        TOGGLE_MUSIC: ('Music: ' + prettyprint.on(settings_list[MUSIC]), 'Turn ' + prettyprint.on(not settings_list[MUSIC]) + ' Music'),
                        EXIT_OPTIONS: ('Back','Go Back to the Option Menu')
                    }
                        
            if option_result == DISPLAY_MENU:
                display_result = True
                last_highlighted = 0

                while display_result:
                    display_result = menu.Menu(screen,
                                               music_list[MENU_MUSIC],
                                               new_scene,
                                               menu_bounds,
                                               ('Video Options', 96, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                                               display_menu_dictionary,
                                               last_highlighted).show()
            
                    if display_result == TOGGLE_PARTICLES:
                        settings_list[PARTICLES] = not settings_list[PARTICLES]
                        last_highlighted = 0
                        
                    elif display_result == TOGGLE_FULLSCREEN:
                        settings_list[SETTING_FULLSCREEN] = not settings_list[SETTING_FULLSCREEN]
                        last_highlighted = 1
                        
                        if settings_list[SETTING_FULLSCREEN]:
                            screen = utility.set_fullscreen()
                        else:
                            screen = utility.set_fullscreen(False)
                            
                        pygame.mouse.set_visible(False)
                    
                    elif display_result == EXIT_OPTIONS:
                        display_result = False
                        
                    display_menu_dictionary = {
                        TOGGLE_PARTICLES: ('Particles: ' + prettyprint.able(settings_list[PARTICLES]), 'Turn ' + prettyprint.on(not settings_list[PARTICLES]) + ' Particle Effects'),
                        TOGGLE_FULLSCREEN: ('Video Mode: ' + prettyprint.screen_mode(settings_list[SETTING_FULLSCREEN]), 'Switch To ' + prettyprint.screen_mode(not settings_list[SETTING_FULLSCREEN]) + ' Mode'),
                        EXIT_OPTIONS: ('Back', 'Go Back to the Main Menu')
                    }
            
            elif option_result == EXIT_OPTIONS:
                option_result = False
            
            elif option_result == CHANGE_SENSITIVITY:
                sensitivity_result = True
                last_highlighted = 0

                while sensitivity_result:
                    sensitivity_menu = menu.Menu(screen,
                                                 music_list[MENU_MUSIC],
                                                 new_scene,
                                                 menu_bounds,
                                                 ('Mouse Sensitivity', 96, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                                                 sensitivity_menu_dictionary,
                                                 last_highlighted)

                    sensitivity_result = sensitivity_menu.show()
                    mouse_sensitivities = [0.5, 0.75, 1, 1.25, 1.5]
                    settings_list[SENSITIVITY] = mouse_sensitivities[sensitivity_result]

                    if sensitivity_result > 0:
                        sensitivity_result = False

            option_menu_dictionary = {
                SOUND_MENU: ('Sound Options', 'Change Sound Options'),
                DISPLAY_MENU: ('Video Options', 'Change Video Options'),
                CHANGE_SENSITIVITY: ('Mouse Sensitivity: ' + prettyprint.mouse_sensitivity(settings_list[SENSITIVITY]), 'Change Mouse Sensitivity'),
                EXIT_OPTIONS: ('Back', 'Go Back to the Main Menu')
            }
            
    elif menu_result == CREDIT_MENU:
        credits.Credits(screen, music_list[MENU_MUSIC])
        
    elif menu_result == EXIT_GAME:
        game_is_running = False
        utility.write_settings()

splashscreen.SplashScreen(screen, 'outroSplash')
quit()
