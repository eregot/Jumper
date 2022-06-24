import pygame
from sys import exit
from random import randint

def display_score():

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            if enemy_rect.bottom == 300: screen.blit(snail_surf,enemy_rect)
            else: screen.blit(fly_surf, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]

        return enemy_list
    else: return []

def collisions(player,enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect): return False
    return True
pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Jump Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/gamefont.ttf',50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#score_surf = test_font.render('Jump Game', False, (64,64,64))
#score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

fly_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

enemy_rect_list = []

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_grav = 0

#INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Jump Game', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,70))

game_message = test_font.render('Press space to play', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

#TIMER
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1400)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): 
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        
        if event.type == enemy_timer and game_active:
            if randint(0,2):
                enemy_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
            else:
                enemy_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))


    if game_active:
        screen.blit(ground_surf,(0,300))
        screen.blit(sky_surf, (0,0))
#        pygame.draw.rect(screen, '#c0e8ec', score_rect)
#        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
#        screen.blit(score_surf, score_rect)
        score = display_score()

        #SNAIL
#        snail_rect.x -= 6
#        if snail_rect.right <= 0: snail_rect.left = 800
#        screen.blit(snail_surf, snail_rect)

        #PLAYER
        player_grav += 1
        player_rect.y += player_grav
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        #ENEMY MOVEMENT
        enemy_rect_list = enemy_movement(enemy_rect_list)

        #COLLISIONS
        game_active = collisions(player_rect, enemy_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        enemy_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

        score_message = test_font.render(f'Your Score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)