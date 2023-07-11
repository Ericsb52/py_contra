import pygame
from settings import *
from tile import *
from player import *


class AllSprites(pg.sprite.Group):
    def __init__(self):
        super(AllSprites, self).__init__()
        self.display_surf = pg.display.get_surface()
        self.offset = Vector2()

        self.fg_sky = pg.image.load("../graphics/sky/fg_sky.png").convert_alpha()
        self.bg_sky = pg.image.load("../graphics/sky/bg_sky.png").convert_alpha()
        self.img_width = self.bg_sky.get_width()

        self.padding = WIDTH / 2
        tmx_map = load_pygame("../data/map.tmx")
        map_width = tmx_map.tilewidth * tmx_map.width + (2*self.padding)
        self.sky_number = int(map_width // self.img_width)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        for x in range(self.sky_number):
            xpos = -self.padding + (x*self.img_width)
            self.display_surf.blit(self.bg_sky, (xpos-self.offset.x /2.5,800-self.offset.y/2.5))
            self.display_surf.blit(self.fg_sky, (xpos - self.offset.x/2, 800 - self.offset.y/2))


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offest_rect = sprite.image.get_rect(center=sprite.rect.center)
            offest_rect.center -= self.offset
            self.display_surf.blit(sprite.image, offest_rect)


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pg.sprite.Group()
        self.platforms_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()



        self.setup()

    def run(self):
        while True:
            # manage clock
            dt = self.clock.tick() / 1000
            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # update
            self.all_sprites.update(dt)

            # draw
            self.screen.fill(sun_set)
            self.all_sprites.custom_draw(self.player)

            pg.display.update()

    def setup(self):

        self.flash_animation_frames = [pg.image.load("../graphics/fire/0.png").convert_alpha(),
                                       pg.image.load("../graphics/fire/1.png").convert_alpha()]
        tmx_map = load_pygame(level_path)
        # tiles
        # collision tiles
        for x, y, surf in tmx_map.get_layer_by_name("Level").tiles():
            CollisionTile((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites,self.collision_sprites])
        # decoration tiles
        i = 0
        layer_index = ["bg", "bg detail", "fg detail bottom", "fg detail top"]
        for layer in ["BG", "BG Detail", "FG Detail Bottom", "FG Detail Top"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS[layer_index[i]])
            i += 1

        # objects

        # player
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(self,(obj.x, obj.y), self.all_sprites, LAYERS["main"],self.collision_sprites)

        # platforms
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name("Platforms"):
            if obj.name == "Platform":
               MovingPlatform(self,(obj.x,obj.y),obj.image,[self.all_sprites,self.collision_sprites,self.platforms_sprites])
            else:
                border_rect = pg.Rect(obj.x,obj.y,obj.width,obj.height)
                self.platform_border_rects.append(border_rect)







if __name__ == "__main__":
    main = Main()
    main.run()
