from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self,game,pos,groups,z,hit_group):
        super(Player, self).__init__(groups)
        self.game = game
        self.import_assets(player_art)

        self.frame_index = 0
        self.status = "right"
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = player_speed
        self.gravity = GRAVITY
        self.jump_speed = player_jump_force
        self.isGrounded = False
        self.isDucking = False
        self.moving_floor = None

        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        self.muzzel = (self.rect.center + self.direction * 60)+self.y_offset


        self.can_shoot = True
        self.last_shoot_time = 0
        self.coolDown = shoot_coolDown

        # collisons
        self.old_rect = self.rect.copy()
        self.collisions_group = hit_group

    def shoot_timer(self):
        if not self.can_shoot:
            cur_time = pg.time.get_ticks()
            if cur_time - self.last_shoot_time > self.coolDown:
                self.last_shoot_time = cur_time
                self.can_shoot = True
    def getStatus(self):
        # Idle
        if self.dir.x == 0 and self.isGrounded:
            self.status = self.status.split("_")[0]+"_idle"
        # Jump
        if self.dir.y != 0 and not self.isGrounded:
            self.status = self.status.split("_")[0]+"_jump"

        # Duck
        if self.isGrounded and self.isDucking:
            self.status = self.status.split("_")[0] + "_duck"
    def check_contact(self):
        bottom_rect = pg.Rect(0,0,self.rect.width,5)
        bottom_rect.midtop = self.rect.midbottom
        for sprite in self.collisions_group:
            if sprite.rect.colliderect(bottom_rect):
                if self.dir.y > 0:
                    self.isGrounded = True
                if hasattr(sprite,"dir"):
                    self.moving_floor = sprite


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

    def animate(self,dt):
        self.frame_index += 7 *dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.dir.x = -1
            self.status = "left"
        elif keys[pg.K_d]:
            self.dir.x = 1
            self.status = "right"
        else:
            self.dir.x = 0
        # jumping
        if keys[pg.K_w] and self.isGrounded:
            self.dir.y = -self.jump_speed
        # ducking
        if keys[pg.K_s]:
            self.isDucking = True
        else:
            self.isDucking = False
        if keys[pg.K_SPACE]:
            if self.can_shoot:
                self.shoot()

    def move(self,dt):
        if self.isDucking and self.isGrounded:
            self.dir.x = 0
        self.pos.x += self.dir.x * self.speed*dt
        self.rect.x = round(self.pos.x)
        self.collisions("horizontal")

        self.dir.y += self.gravity
        self.pos.y += self.dir.y * dt
        if self.moving_floor and self.moving_floor.dir.y and self.dir.y > 0:
            self.dir.y= 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.isGrounded = True
        self.rect.y = round(self.pos.y)
        self.collisions("vertical")
        self.moving_floor = None

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
                    # top collisions
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.isGrounded = True
                    # bottom collisions
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.dir.y = 0
        if self.isGrounded and self.dir.y != 0:
            self.isGrounded = False

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.shoot_timer()
        self.input()
        self.getStatus()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        self.update_muzzel()
    def update_muzzel(self):
        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        if "right" in self.status:
            self.muzzel = (self.rect.center + self.direction * 75) + self.y_offset
        else:
            self.muzzel = (self.rect.center + self.direction * 45) + self.y_offset
        if self.isDucking:
            self.muzzel = (self.rect.center + self.direction * 60) + self.y_offset

    def shoot(self):
        self.can_shoot = False
        Bullet(self.game,self.muzzel,self.direction,[self.game.all_sprites,self.game.bullet_sprites],self)

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
    def __init__(self,game,pos,dir,groups,owner):
        super().__init__(groups)
        self.game = game
        self.owner = owner
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
        Fire_Animation(self.game,self.owner,self.owner.direction,self.game.all_sprites)

    def update(self,dt):
        self.pos += self.dir * self.speed * dt
        self.rect.center = (round(self.pos.x),round(self.pos.y))


        if pg.time.get_ticks() - self.start_time > self.life_time:
            self.kill()
        hits = pg.sprite.spritecollide(self,self.game.collision_sprites,False)
        if hits:
            self.kill()




