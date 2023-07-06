from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self,pos,groups,z):
        super(Player, self).__init__(groups)
        self.image = pg.Surface((40,80))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = player_speed

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.dir.x = -1
        elif keys[pg.K_d]:
            self.dir.x = 1
        else:
            self.dir.x = 0

        if keys[pg.K_w]:
            self.dir.y = -1
        elif keys[pg.K_s]:
            self.dir.y = 1
        else:
            self.dir.y = 0



    def move(self,dt):
        self.pos.x += self.dir.x * self.speed*dt
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def update(self,dt):
        self.input()
        self.move(dt)
