import pygame
import antigravity
import random
import time

pygame.init()

SCREEN_SIZE = SCREEN_WIDHT, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SCREEN_SIZE)


all_sprites = pygame.sprite.Group()
meteorites = pygame.sprite.Group()

clock = pygame.time.Clock()


def set_coin_pos(alien, coin):
    coin.rect.x = random.randint(0, SCREEN_WIDHT - coin.rect.width)
    coin.rect.y = random.randint(0, SCREEN_HEIGHT - coin.rect.height)
    if pygame.sprite.collide_mask(alien, coin):
        set_coin_pos(alien, coin)


def game():
    score = 0
    game_paused = 0
    prochnost = random.randint(10, 50)
    font = pygame.font.SysFont('Arial', 45)
    alien = pygame.sprite.Sprite(all_sprites)
    alien.image = pygame.image.load('alien.png')
    alien.rect = alien.image.get_rect()
    coin = pygame.sprite.Sprite(all_sprites)
    coin.image = pygame.image.load('coin.png')
    coin.rect = coin.image.get_rect()
    set_coin_pos(alien, coin)
    sound = pygame.mixer.Sound('kill.mp3')
    sound = pygame.mixer.Sound('kill.mp3')
    alien_speed = 5
    run = True
    time_clock = pygame.time.get_ticks()
    game_over = False
    
    while run:
        text = font.render(f'Убито криперов: {score}', False, (0, 120, 0))
        t = font.render(f'Меч сломался {score}', False, (255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = not game_paused

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if alien.rect.left > 0:
                alien.rect.left -= alien_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if alien.rect.right < SCREEN_WIDHT:
                alien.rect.right += alien_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if alien.rect.top > 0:
                alien.rect.top -= alien_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if alien.rect.bottom < SCREEN_HEIGHT:
                alien.rect.bottom += alien_speed
        screen.fill((140, 80, 0))
        if game_paused:
            alien_speed = 0
            pause = font.render('Пауза                ', False, (200, 200, 200))
            screen.blit(pause, (5, 200))
        else:
            alien_speed = 5
            pause = font.render('', False, (255, 255, 255))
        if pygame.sprite.collide_mask(alien, coin):
            set_coin_pos(alien, coin)
            score += 1
            sound.play()
            prochnost -= 1
            if prochnost == 0:
                screen.blit(t, (0, 0))
                time.sleep(3)
                break
        if game_paused: continue
        
        if (pygame.time.get_ticks() - time_clock) / 1000 > 3:
            meteor = pygame.sprite.Sprite(meteorites)
            meteor.image = pygame.image.load("meteor.png")
            meteor.rect = meteor.image.get_rect()
            meteor.rect.x = random.randint(0, SCREEN_HEIGHT)
            meteor.rect.y = -20
            time_clock = pygame.time.get_ticks()

        for meteor in meteorites:
            meteor.rect.y += 5
            if pygame.sprite.collide_mask(alien, meteor):
                sound.play()
                game_over = True
                time.sleep(2)
    
        if not game_over:
            screen.blit(text, (5, 5))
            all_sprites.draw(screen)
            meteorites.draw(screen)
        else:
            text = font.render('Гаме овер!', False, (255, 0, 0))
            screen.blit(text, (280, 250))
        clock.tick(24)
        pygame.display.update()
        
game()

pygame.quit()
