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
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

# player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'player_sprite.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(25, 10)
PLAYER_HEALTH = 100

# gun settings
BULLET_IMG = 'projectile.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 300
RECOIL = 100
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# mob settings
MOB_IMG = 'mob_sprite.png'
MOB_SPEEDS = [125, 150, 175, 200]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400
SPLAT = 'mob_splat.png'

# effects
MUZZLE_FLASHES = ['white_puff1.png', 'white_puff2.png', 'white_puff3.png', 'white_puff4.png']
FLASH_DURATION = 40

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 1
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# items
ITEM_IMAGES = {'health': 'health_pack.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# sounds and music
BG_MUSIC = 'bgm.ogg'
PLAYER_HIT_SOUNDS = ['player/hit_1.wav', 'player/hit_2.wav',
                    'player/hit_3.wav', 'player/hit_4.wav',
                    'player/hit_5.wav', 'player/hit_6.wav', 'player/hit_7.wav']
MOB_NOISE_SOUNDS = ['mob/noise1.wav', 'mob/noise2.wav', 'mob/noise3.wav',
                    'mob/noise4.wav', 'mob/noise5.wav']
MOB_HIT_SOUNDS = ['mob_hit.wav']
MOB_DEATH_SOUNDS = ['mob_death.wav']
WEAPON_SOUNDS = ['weapon_shot.wav']
EFFECT_SOUNDS = {'level_start': 'level_start.wav',
                'health_up': 'health_pack.wav'}