from settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,game,pos,groups,z,path):
        super().__init__(groups)
        self.game = game
        self.import_assets(path)
        self.frame_index = 0
        self.status = "right"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z
        self.mask = pg.mask.from_surface(self.image)
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = player_speed
        self.can_shoot = True
        self.last_shoot_time = 0
        self.coolDown = shoot_coolDown
        self.isDucking = False
        self.health = 3
        self.is_safe = False
        self.invincable_time = 300
        self.hit_time = 0
        self.hit_sound = pg.mixer.Sound("../audio/bullet.wav")
        self.hit_sound.set_volume(0.2)
        self.shoot_sound = pg.mixer.Sound("../audio/hit.wav")
        self.shoot_sound.set_volume(0.2)


    def blink(self):
        if self.is_safe:
            if self.wave_value():
                mask = pg.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False
    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split(".")[0])):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)

    def shoot_timer(self):
        if not self.can_shoot:
            cur_time = pg.time.get_ticks()
            if cur_time - self.last_shoot_time > self.coolDown:
                self.last_shoot_time = cur_time
                self.can_shoot = True
    def invicable_timer(self):
        if self.is_safe:
            cur_time = pg.time.get_ticks()
            if cur_time - self.hit_time > self.invincable_time:
                self.hit_time = cur_time
                self.is_safe = False



    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

class Fire_Animation(pg.sprite.Sprite):
    def __init__(self,game,owner,dir,groups):
        super().__init__(groups)
        self.game = game
        self.owner = owner
        self.frames = self.game.flash_animation_frames
        if dir.x < 0:
            self.frames = [pg.transform.flip(frame,True,False) for frame in self.frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = self.owner.muzzel)
        self.z = LAYERS["main"]

    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    def move(self):
        self.rect.center = self.game.player.muzzel

    def update(self,dt):
        self.animate(dt)
        self.move()

class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir,owner):
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self)
        if owner.type == "player":
            self.owner = self.game.player
            self.game.bullet_sprites.add(self)
        else:
            self.owner = owner
            self.game.enemy_bullets.add(self)


        self.image = pg.image.load(bullet_path).convert_alpha()
        if dir.x < 0:
            self.image = pg.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center = pos)
        self.dir = dir
        self.speed = bullet_speed
        self.pos = pos
        self.z = LAYERS["main"]
        self.start_time = pg.time.get_ticks()
        self.life_time = bullet_life_time


    def update(self,dt):
        self.pos += self.dir * self.speed * dt
        self.rect.center = (round(self.pos.x),round(self.pos.y))


        if pg.time.get_ticks() - self.start_time > self.life_time:
            self.kill()
        hits = pg.sprite.spritecollide(self,self.game.collision_sprites,False)
        if hits:
            self.kill()



