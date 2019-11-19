import os
import pygame as pg

from . import tools


SCREEN_SIZE = (1600, 1000)
ORIGINAL_CAPTION = 'Mazes'

# pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

_SUB_DIRECTORIES = ['ui']
GFX = tools.graphics_from_directories(_SUB_DIRECTORIES)

# FONTS_PATH = os.path.join('resources', 'fonts')
# FONTS = tools.load_all_fonts(FONTS_PATH)

# sfx_path = os.path.join('resources', 'sounds')
# SFX = tools.load_all_sfx(sfx_path)

# music_path = os.path.join('resources', 'music')
# MUSIC = tools.load_all_music(music_path)
