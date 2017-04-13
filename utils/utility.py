import os

import pygame

from utils.settings import *

sound_active = True


def make_bool(value):
    v = value.upper().strip()
    return v == 'TRUE' or value == '1' or value == 'T'


def read_high_scores():
    score_list = []

    try:
        score_file = open(get_path() + '/score.bzd', 'r')
        score_list.append(int(score_file.readline()))
        score_list.append(int(score_file.readline()))
        score_list.append(int(score_file.readline()))
        score_list.append(int(score_file.readline()))
        score_file.close()

        return score_list
    
    except:
        score_file = open(get_path() + '/score.bzd', 'w')
        score_file.write('0\n')
        score_file.write('0\n')
        score_file.write('0\n')
        score_file.write('0\n')
        score_file.close()
        
        return 0, 0, 0, 0


def write_high_scores(scores):
    score_file = open(get_path() + '/score.bzd', 'w')
    score_file.write(str(scores[TUTORIAL_HIGH_SCORE]) + '\n')
    score_file.write(str(scores[WORLD_1_HIGH_SCORE]) + '\n')
    score_file.write(str(scores[WORLD_2_HIGH_SCORE]) + '\n')
    score_file.write(str(scores[WORLD_3_HIGH_SCORE]) + '\n')
    score_file.close()


def read_settings():
    temp_list = []
    try:
        settings_file = open(get_path() + '/settings.bzd', 'r')
        temp_list.append(make_bool(settings_file.readline()))
        temp_list.append(make_bool(settings_file.readline()))
        temp_list.append(make_bool(settings_file.readline()))
        temp_list.append(int(settings_file.readline()))
        temp_list.append(float(settings_file.readline()))
        temp_list.append(make_bool(settings_file.readline()))
        settings_file.close()
        
        for setting in temp_list:
            settings_list.append(setting)

    except:
        print('Missing or Corrupted File: Restoring Defaults')
        temp_list = [True, True, True, 0, 1, True]

        for setting in temp_list:
            settings_list.append(setting)

        write_settings()


def write_settings():
    settings_file = open(get_path() + '/settings.bzd', 'w')
    for element in settings_list:
        settings_file.write(str(element) + '\n')


def get_path():
    """This figures out the 'home' path. Useful for
    storing config/save stuff."""
    
    pathname = ''
    try:
        pathname = os.environ['HOME'] + '/.battlezero'

    except:
        try:
            pathname = os.environ['APPDATA'] + '/battlezero'

        except:
            print('Could not get environment variable for home directory')
            pathname = '.'

    if not os.path.exists(pathname):
        os.mkdir(pathname)

    return pathname


def load_image(name):
    filepath = 'data/images/' + name + '.bzi'

    if os.path.isfile(filepath):
        return pygame.image.load(filepath).convert_alpha()

    else:
        filepath = 'data/images/' + name + '.png'
    
    return pygame.image.load(filepath).convert_alpha()


def load_sound(name):
    filepath = 'data/sounds/' + name + '.bza'

    if os.path.isfile(filepath):
        return pygame.mixer.Sound(filepath)

    else:
        filepath = 'data/sounds/' + name + '.ogg'

    return pygame.mixer.Sound(filepath)


def play_sound(sound, channel_number = None):
    if settings_list[SFX] and sound_active:
        if channel_number:
            pygame.mixer.Channel(channel_number).play(sound)

        else:
            sound.play()


def play_music(music, force_next=True):
    if settings_list[MUSIC] and sound_active:
        if force_next:
            pygame.mixer.Channel(MUSIC_CHANNEL).queue(music)

        elif not pygame.mixer.Channel(MUSIC_CHANNEL).get_queue():
            pygame.mixer.Channel(MUSIC_CHANNEL).queue(music)


def fade_music():
    if sound_active:
        pygame.mixer.Channel(MUSIC_CHANNEL).fadeout(2000)


def dim(dim_value, color_value=(0, 0, 0)):
    dim = pygame.Surface(pygame.display.get_surface().get_size())
    dim.fill(color_value)
    dim.set_alpha(dim_value)
    pygame.display.get_surface().blit(dim,pygame.display.get_surface().get_rect())


def dim_surface(dim_value, color_value=(0, 0, 0)):
    dim = pygame.Surface(pygame.display.get_surface().get_size())
    dim.fill(color_value)
    dim.set_alpha(dim_value)

    return dim


def set_fullscreen(full=True):
    """Creates a display surface either full screen or windowed."""

    if full:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    else:
        return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
