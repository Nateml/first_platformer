import sys
# Allow to import files from current working directory
sys.path.append(".")

import itertools

# Import shared modules and important constants and stuff
from share import *


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("/home/natem/Downloads/platformer_bg.png")

# Import sprites
from sprites import Player, Platform

colours = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])

clock = pygame.time.Clock()

score = 0

base_colour = next(colours)
next_colour = next(colours)
current_colour = base_colour

change_every_x_seconds = 0.2
number_of_steps = change_every_x_seconds * FRAMERATE
step = 1

ADDPLATFORM = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPLATFORM, 1000)

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
platform = Platform()

platforms = pygame.sprite.Group()
platforms.add(platform)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platform)

font = pygame.font.SysFont('Arial', 24)

running = True
while running:
    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                player.jumping = True
            if event.key == K_x:
                bullet_list = player.shoot()
                for bullet in bullet_list:
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        elif event.type == QUIT:
            running = False

        elif event.type == ADDPLATFORM:
            new_platform = Platform()
            platforms.add(new_platform)
            all_sprites.add(new_platform)
            if new_platform.enemy != None:
                enemies.add(new_platform.enemy) 
                all_sprites.add(new_platform.enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    bullets.update()
    platforms.update()

    score_display = font.render('Score: {s}'.format(s=score), True, pygame.color.Color('black'))

    step += 1
    if step < number_of_steps:
        # below is from stack overflow
        # (y-x)/number_of_steps calcs the amount of change per steps required to fade on channel of the old colour to the new colour
        # we multiply it with the current step counter
        current_colour = [x + (((y-x)/number_of_steps)*step) for x, y in zip(pygame.color.Color(base_colour), pygame.color.Color(next_colour))]
    else:
        step = 1
        base_colour = next_colour
        next_colour = next(colours)

    # player_center = (
        # (SCREEN_WIDTH-player.surf.get_width())/2,
        # (SCREEN_WIDTH-player.surf.get_height())/2
    # )

    if player.rect.top > SCREEN_HEIGHT:
        running = False

    if pygame.sprite.spritecollideany(player, platforms):
        score += 1
        player.set_no_v_movement()
        player.reset_jump()
    else:
        player.falling = True
        # pass

    if pygame.sprite.spritecollideany(player, enemies):
       running = False 

    for bullet in bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect(bullet, enemy):
               enemy.platform.kill_enemy() 

    # screen.fill(current_colour)

    # screen.blit(player.image, player.rect)

    for entity in all_sprites:
        try:
            screen.blit(entity.image, entity.rect)
        except Exception:
            screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    # maintain framerate
    clock.tick(FRAMERATE)
