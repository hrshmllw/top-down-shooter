import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

# game class
class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        # folder loading
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        sound_folder = path.join(game_folder, 'sound')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        # UI / font load
        self.title_font = path.join(img_folder, 'game_font.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        # sprite images load
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        # gun shot effects
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # night / light effects
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # sound load
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECT_SOUNDS:
            game_sfx = pg.mixer.Sound(path.join(sound_folder, EFFECT_SOUNDS[type]))
            game_sfx.set_volume(0.2)
            self.effects_sounds[type] = game_sfx
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for sound in WEAPON_SOUNDS[weapon]:
                weapon_sfx = pg.mixer.Sound(path.join(sound_folder, sound))
                if weapon == 'shotgun':
                    weapon_sfx.set_volume(0.04)
                else:
                    weapon_sfx.set_volume(0.2)
                self.weapon_sounds[weapon].append(weapon_sfx)
        self.mob_sounds = []
        for sound in MOB_NOISE_SOUNDS:
            mob_sfx = pg.mixer.Sound(path.join(sound_folder, sound))
            mob_sfx.set_volume(0.2)
            self.mob_sounds.append(mob_sfx)
        self.player_hit_sounds = []
        for sound in PLAYER_HIT_SOUNDS:
            player_sfx = pg.mixer.Sound(path.join(sound_folder, sound))
            player_sfx.set_volume(0.2)
            self.player_hit_sounds.append(player_sfx)
        self.mob_hit_sounds = []
        for sound in MOB_HIT_SOUNDS:
            mob_hit_sfx = pg.mixer.Sound(path.join(sound_folder, sound))
            mob_hit_sfx.set_volume(0.1)
            self.mob_hit_sounds.append(mob_hit_sfx)
        self.mob_death_sounds = []
        for sound in MOB_DEATH_SOUNDS:
            mob_death_sfx = pg.mixer.Sound(path.join(sound_folder, sound))
            mob_death_sfx.set_volume(0.2)
            self.mob_death_sounds.append(mob_death_sfx)
        
    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'tilemap1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'mob':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.grid = False
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            choice(self.mob_hit_sounds).play()
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draws light gradient onto fog image / rectangle
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw_player_health(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.7:
            col = GREEN
        elif pct > 0.35:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        if self.grid:
            self.draw_grid()
        if self.night:
            self.render_fog()
        # player HUD
        self.draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        self.draw_text('Enemies: {}'.format(len(self.mobs)), self.title_font, 30, WHITE,
                        WIDTH - 10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("PAUSED", self.title_font, 105, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_g:
                    self.grid = not self.grid
                if event.key == pg.K_n:
                    self.night = not self.night

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("W or UP - Move forward", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 1 / 10 , align="center")
        self.draw_text("A/D or LEFT/RIGHT - Turn left/right", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 2 / 10 , align="center")
        self.draw_text("S or DOWN - Move backward", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 3 / 10 , align="center")
        self.draw_text("SPACE - Shoot", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 4 / 10 , align="center")
        self.draw_text("N - Toggle night mode", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 5 / 10 , align="center")
        self.draw_text("G - Toggle grid mode", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 6 / 10 , align="center")
        self.draw_text("H - Toggle hit boxes", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 7 / 10 , align="center")
        self.draw_text("ESC - Quit game", self.title_font, 20, WHITE,
                        WIDTH / 2, HEIGHT * 8 / 10 , align="center")
        self.draw_text("Press any key to start game", self.title_font, 35, WHITE,
                        WIDTH / 2, HEIGHT * 9 / 10, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, WHITE,
                        WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press any key to play again.", self.title_font, 30, WHITE,
                        WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()