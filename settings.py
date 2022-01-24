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

# weapon settings
BULLET_IMG = 'projectile.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                    'bullet_lifetime': 1000,
                    'bullet_rate': 250,
                    'recoil': 100,
                    'bullet_spread': 5,
                    'bullet_damage': 10,
                    'bullet_size': 'lg',
                    'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 650,
                    'bullet_lifetime': 400,
                    'bullet_rate': 1100,
                    'recoil': 300,
                    'bullet_spread': 20,
                    'bullet_damage': 5,
                    'bullet_size': 'sm',
                    'bullet_count': 12}

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
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

# environment
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = 'light.png'

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 1
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# items
ITEM_IMAGES = {'health': 'health_pack.png',
                'shotgun': 'obj_shotgun.png'}
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
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                'shotgun': ['shotgun.wav']}
EFFECT_SOUNDS = {'level_start': 'level_start.wav',
                'health_up': 'health_pack.wav',
                'gun_pickup': 'gun_pickup.wav'}