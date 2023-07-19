from settings import *
from entity import *

class Enemy(Entity):
    def __init__(self,game,pos,groups,z,path):
        super().__init__(game,pos,groups,z,path)
        self.player = self.game.player
        for sprite in self.game.collision_sprites:
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top
        self.coolDown = enemy_shoot_coolDown
        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        self.muzzel = self.rect.center
        self.type = "enemy"
        self.invincable_time = 200
    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = "left"
        else:
            self.status = "right"

    def take_damage(self):
        self.hit_sound.play()
        self.is_safe = True
        self.health -= 1

    def die(self):
        self.kill()
    def check_fire(self):
        enemy_pos = Vector2(self.rect.center)
        player_pos = Vector2(self.player.rect.center)
        distance = (player_pos-enemy_pos).magnitude()
        same_y = True if self.rect.top -20 < player_pos.y <self.rect.bottom +20 else False
        if distance < 500 and same_y and self.can_shoot:
            self.shoot(self)


    def update_muzzel(self):
        self.direction = Vector2(1, 0) if self.status.split("_")[0] == "right" else Vector2(-1, 0)
        self.y_offset = Vector2(0 - 16) if not self.isDucking else Vector2(0, 10)
        if "right" in self.status:
            self.muzzel = (self.rect.center + self.direction * 75) + self.y_offset
        else:
            self.muzzel = (self.rect.center + self.direction * 45) + self.y_offset
        if self.isDucking:
            self.muzzel = (self.rect.center + self.direction * 60) + self.y_offset

    def shoot(self, owner):
        self.shoot_sound.play()
        self.can_shoot = False
        Bullet(self.game, self.muzzel, self.direction, owner)


    def update(self,dt):
        self.get_status()
        self.shoot_timer()
        self.animate(dt)
        self.blink()
        self.update_muzzel()
        self.check_fire()
        hits = pg.sprite.spritecollide(self, self.game.bullet_sprites, True,pg.sprite.collide_mask)
        if hits:
            self.take_damage()

        if self.health <= 0:
            self.die()



