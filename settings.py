import pygame as pg
vec = pg.math.Vector2

# color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
BGCOLOR = LIGHTGREY
TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'player_sprite.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(25, 10)

# gun settings
BULLET_IMG = 'projectile.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
RECOIL = 200
GUN_SPREAD = 5

# mob settings
MOB_IMG = 'mob_sprite.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)

# environment settings
WALL_IMG = 'wall_sprite.png'
