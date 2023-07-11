import pygame as pg
import sys
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from os import walk


# game settings
TITLE = "PY Contra"
FPS = 60
TILE_SIZE = 64

# custom colors
sun_set = (249,131,103)

# screen settings
WIDTH = 1280
HEIGHT = 720

# layers
LAYERS = {"bg":0,
          "bg detail":1,
          "main":2,
          "fg detail bottom":3,
          "fg detail top":4,
          "hud":5
          }


# map path
level_path = "../data/map.tmx"


# player settings
player_speed = 400
player_jump_force = 1400
GRAVITY = 15
player_art = "../graphics/player"
shoot_coolDown = 200

# platform settings
plat_speed = 200

# bullet settings
bullet_speed = 1200
bullet_path = "../graphics/bullet.png"
bullet_life_time = 500







