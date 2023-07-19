
from settings import *

class Overlay:
    def __init__(self,game):
        self.game = game
        self.player = self.game.player
        self.screen = pg.display.get_surface()
        self.health_surf = pg.image.load("../graphics/health.png").convert_alpha()

    def display(self):

        for i in range(self.player.health):
            xpos = 10+i*(self.health_surf.get_width()+1)
            ypos = 10
            self.screen.blit(self.health_surf,(xpos,ypos))


