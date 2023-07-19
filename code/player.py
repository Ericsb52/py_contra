from settings import *
from entity import *

class Player(Entity):
    def __init__(self,game,pos,groups,z,path):
        super(Player, self).__init__(game,pos,groups,z,path)

        self.gravity = GRAVITY
        self.jump_speed = player_jump_force
        self.isGrounded = False
        self.moving_floor = None
        # collisons
        self.collisions_group = self.game.collision_sprites
        self.type = "player"
        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        self.muzzel = (self.rect.center + self.direction * 60) + self.y_offset
        self.health = 10



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

    def update_muzzel(self):
        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        if "right" in self.status:
            self.muzzel = (self.rect.center + self.direction * 75) + self.y_offset
        else:
            self.muzzel = (self.rect.center + self.direction * 45) + self.y_offset
        if self.isDucking:
            self.muzzel = (self.rect.center + self.direction * 60) + self.y_offset

    def shoot(self,owner):
        self.shoot_sound.play()
        self.can_shoot = False
        Bullet(self.game,self.muzzel,self.direction,owner)
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
        if keys[pg.K_s] and self.isGrounded:
            self.isDucking = True
        else:
            self.isDucking = False
        if keys[pg.K_SPACE]:
            if self.can_shoot:
                Fire_Animation(self.game, self, self.direction, self.game.all_sprites)
                self.shoot(self)


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
    def take_damage(self):
        self.hit_sound.play()
        self.is_safe = True
        self.health -= 1

    def die(self):
        pg.quit()
        sys.exit()

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.shoot_timer()
        self.invicable_timer()
        self.input()
        self.getStatus()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        self.blink()
        self.update_muzzel()
        hits = pg.sprite.spritecollide(self.game.player,self.game.enemy_bullets,True,pg.sprite.collide_mask)
        if hits and not self.is_safe:
            self.take_damage()

        if self.health <= 0:
            self.die()







