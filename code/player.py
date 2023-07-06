from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self,pos,groups,z,hit_group):
        super(Player, self).__init__(groups)
        self.import_assets(player_art)

        self.frame_index = 0
        self.status = "right"
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = player_speed

        # collisons
        self.old_rect = self.rect.copy()
        self.collisions_group = hit_group


    def import_assets(self,path):
        self.animations = {}
        for index,folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key =  lambda string: int(string.split(".")[0])):
                    path = folder[0].replace("\\","/")+"/"+file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)
        print(self.animations)
    def animate(self,dt):
        self.frame_index += 7 *dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
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
        self.collisions("horizontal")

        self.pos.y += self.dir.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collisions("vertical")

    def collisions(self,direction):
        for sprite in self.collisions_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    # left collisions
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collisions
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    self.pos.x = self.rect.x

                else:
                    pass
    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)

        self.animate(dt)
