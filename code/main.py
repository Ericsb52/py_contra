import pygame
from settings import *
from tile import *
from player import *


class AllSprites(pg.sprite.Group):
    def __init__(self):
        super(AllSprites, self).__init__()
        self.display_surf = pg.display.get_surface()
        self.offset = Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):
            offest_rect = sprite.image.get_rect(center = sprite.rect.center)
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
        self.setup()

    def run(self):
        while True:
            # manage clock
            dt = self.clock.tick(FPS) / 1000
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

        tmx_map = load_pygame(level_path)
        # tiles
        for x, y, surf in tmx_map.get_layer_by_name("Level").tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,LAYERS["main"])
        i = 0
        layer_index = ["bg","bg detail","fg detail bottom","fg detail top"]
        for layer in ["BG","BG Detail","FG Detail Bottom","FG Detail Top"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,LAYERS[layer_index[i]])
            i+=1

        # objects
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites,LAYERS["main"])


if __name__ == "__main__":
    main = Main()
    main.run()
