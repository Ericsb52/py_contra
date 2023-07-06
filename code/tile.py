from settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,surf,groups,z):
        super(Tile, self).__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z