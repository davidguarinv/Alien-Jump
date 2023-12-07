import pygame
from sys import exit
from random import randint



def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}',False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list: 
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init() 
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Alien Jump') 
clock = pygame.time.Clock() #Frame rate
font = pygame.font.Font('Pixeltype.ttf',64)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

#Obstacle
snail_frame_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha() #Helps pygame process it better and faster. 
snail_frame_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha() #Helps pygame process it better and faster. 
snail_frames = [snail_frame_1,snail_frame_2]
snail_index = 0
snail_surface = snail_frames[snail_index]

fly_frame_1= pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
fly_frame_2= pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_index = 0
fly_surface = fly_frames[fly_index]

obstacle_rect_list = []

#Player
player_walk1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('Graphics/player/jump.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))

player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))
title_surface = font.render('Alien Jump', False, (64,64,64))
title_rect = title_surface.get_rect(midbottom = (400,90))
instruct_surf = font.render('Press SPACE to start', False, (64,64,64))
instruct_rect = instruct_surf.get_rect(midbottom = (400,360))  

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,5000)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,100)


while True:
    #Game loop should have two elements: input and draw

    for event in pygame.event.get(): #check inputs
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #Safe way to completely exit all code
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom ==  300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:    
            if event.type == obstacle_timer:
                if randint(0,2): obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100),300)))
                else: obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100),210)))
            
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surface = snail_frames[snail_index]
            
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surface = fly_frames[fly_index]
                
                                  
    if game_active:
        #draw elements
        #update everything

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list) 

        #Collision
        game_active = collision(player_rect,obstacle_rect_list)
    

    else:
        screen.fill('#ADD8E6')
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = font.render(f'Score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,360))

        screen.blit(title_surface,title_rect)

        if score == 0: screen.blit(instruct_surf,instruct_rect)
        else: screen.blit(score_message,score_message_rect)


    pygame.display.update()
    clock.tick(60) #60 times per second: frame rate




    '''
    Method for key pressing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:

    #Snail collision with player

    if player_rect.colliderect(snail_rect): #rect1.collidepoint((x,y)) hel
        print('collision')

    #Mouse collision with player with pygame.mouse
    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed())


    So, why have two ways? The pygame methods are great when using other classes. 
    Event loop is used now for simplicity. 
    
    pygame event. Does the same thing as using pygame.mouse
        if event.type == pygame.MOUSEMOTION:
            if player_rect.collidepoint(event.pos):
                print ('collision')
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('*Mouse click*')
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('*Mouse de-click*')

    '''
