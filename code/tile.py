from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super(Tile, self).__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        print(groups)
        super().__init__(pos, surf, groups, LAYERS["main"])
        self.old_rect = self.rect.copy()

class MovingPlatform(CollisionTile):
    def __init__(self,game,pos,surf,groups):
        super().__init__(pos,surf,groups)
        self.game = game
        self.dir = Vector2(0,-1)
        self.speed = plat_speed
        self.pos = Vector2(self.rect.topleft)
        self.old_rect = self.rect.copy()

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.dir.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.platform_colisions()

    def platform_colisions(self):
        for platform in self.game.platforms_sprites.sprites():
            for border in self.game.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.dir.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.dir.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.dir.y = -1
            if platform.rect.colliderect(self.game.player.rect) and self.game.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.game.player.rect.top
                platform.pos.y = platform.rect.y
                platform.dir.y = -1