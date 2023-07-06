from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super(Tile, self).__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super(Tile, self).__init__(pos, surf, groups, LAYERS["main"])
        self.old_rect = self.rect.copy()
