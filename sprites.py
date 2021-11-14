import sys
import os.path

sys.path.append(".")

from share import *
import random

SPRITE_PLAYER_IMAGE = pygame.image.load(os.path.join('images', 'sprite1.png'))
SPRITE_PLATFORM_IMAGE = pygame.image.load(os.path.join('images', 'sprite_platform.png')).convert_alpha();
SPRITE_ENEMY_IMAGE1 = pygame.transform.scale(pygame.image.load(os.path.join('images', 'sprite_enemy1.png')), (70, 80))
SPRITE_ENEMY_IMAGE2 = pygame.transform.scale(pygame.image.load(os.path.join('images', 'sprite_enemy2.png')), (70, 80))
SPRITE_ENEMY_IMAGE3 = pygame.transform.scale(pygame.image.load(os.path.join('images', 'sprite_enemy3.png')), (70, 80))
SPRITE_ENEMY_IMAGE4 = pygame.transform.scale(pygame.image.load(os.path.join('images', 'sprite_enemy4.png')), (70, 80))

class Enemy(pygame.sprite.Sprite):
    width = 70
    height = 80
    colour = pygame.color.Color("red")
    def __init__(self, center, platform):
        super(Enemy, self).__init__()
        self.platform = platform
        # self.surf = pygame.Surface((self.width, self.height))
        # self.surf.fill(self.colour)
        randNum = random.randint(1, 4)
        if (randNum == 1):
           self.image = SPRITE_ENEMY_IMAGE1
        elif (randNum == 2):
           self.image = SPRITE_ENEMY_IMAGE2
        elif (randNum == 3):
           self.image = SPRITE_ENEMY_IMAGE3
        elif (randNum == 4):
           self.image = SPRITE_ENEMY_IMAGE4
        else:
           self.image = SPRITE_ENEMY_IMAGE1

        self.rect = self.image.get_rect(center=(center[0], center[1]-self.height/2))

class Bullet(pygame.sprite.Sprite):
    width = 8
    height = 4
    speed = 15
    colour = pygame.color.Color("red")
    def __init__(self, direction, center):
        super(Bullet, self).__init__()
        self.direction = direction # 1 (right) or -1 (left)
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.colour)

        self.rect = self.surf.get_rect(center=center)

    def update(self):
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Player(pygame.sprite.Sprite):
    jumping = False
    falling = False
    prev_fall = 0
    terminal_velocity = 20
    gravity = 0.5
    jump_strength = 25
    has_jump = True
    speed = 8
    vertical_movement=0
    keybinds = {
        "left": [K_a, K_LEFT],
        "right": [K_d, K_RIGHT],
        "jump": [K_SPACE]
    }
    bullets = set()

    def __init__(self):
        super(Player, self).__init__()
        self.image = SPRITE_PLAYER_IMAGE;
        # self.surf = pygame.Surface((30, 100))
        # self.surf.fill((200, 200, 200))
        # self.rect = self.image.get_rect(center=pos)
        self.rect = self.image.get_rect(
            center=(
                (SCREEN_WIDTH-self.image.get_width())/2,
                (SCREEN_HEIGHT-self.image.get_height())/2
            )
        )

    def update(self, pressed_keys):
        for key in self.keybinds["jump"]:
            if pressed_keys[key]:
                if not self.jumping and self.has_jump:
                    self.vertical_movement = self.jump_strength * -1
                    self.falling = False
                    self.jumping = True
                    self.has_jump = False
        for key in self.keybinds["right"]:
            if pressed_keys[key]:
                self.rect.move_ip(self.speed, 0)
        for key in self.keybinds["left"]:
            if pressed_keys[key]:
                self.rect.move_ip(self.speed * -1, 0)

        if self.jumping:
            self.vertical_movement += self.gravity
            if self.vertical_movement >= 0:
                self.jumping = False
                self.falling = True
            self.rect.move_ip(0, self.vertical_movement)
        if self.falling:
            self.vertical_movement += self.gravity
            if self.vertical_movement >= self.terminal_velocity:
                self.vertical_movement = self.terminal_velocity
            self.rect.move_ip(0, self.vertical_movement)

    def set_no_v_movement(self):
        self.jumping = False
        self.falling = False
        self.vertical_movement = 0

    def reset_jump(self):
        self.has_jump = True

    def shoot(self):
        self.bullets.add(Bullet(direction=1, center=(self.rect.center)))
        return self.bullets



class Platform(pygame.sprite.Sprite):
    width = 200
    height = 10
    speed = 5
    def __init__(self):
        super(Platform, self).__init__()

        # self.surf = pygame.Surface((self.width, self.height))
        self.image = SPRITE_PLATFORM_IMAGE;
        # self.surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        # self.surf.fill((0, 0, 0))
        self.rect = self.image.get_rect(
            center=(
                (SCREEN_WIDTH) + self.image.get_width(),
                random.randint(self.image.get_height(),int(SCREEN_HEIGHT-self.image.get_height()))
            )
        )
        if (random.randint(0, 4) == 1):
            self.enemy = Enemy(center=(self.rect.center[0], self.rect.center[1]-self.height), platform=self)
        else:
            self.enemy = None

    def update(self):
        self.rect.move_ip(self.speed * -1, 0)
        if (self.enemy != None):
            self.enemy.rect.move_ip(self.speed * -1, 0)
        if self.rect.right < 0:
            self.kill()

    def kill_enemy(self):
        if (self.enemy != None):
            self.enemy.kill()



