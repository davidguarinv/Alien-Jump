import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('Graphics/player/jump.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
    
    def player_input(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
           self.jump_sound.play()
           self.gravity = -20
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__ (self,type):
        super().__init__()
        if type == 'fly':
            fly_1= pygame.image.load('Graphics/fly/fly1.png').convert_alpha()
            fly_2= pygame.image.load('Graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha() #Helps pygame process it better and faster. 
            snail_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha() #Helps pygame process it better and faster. 
            self.frames = [snail_1,snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}',False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    
    
    else: return True


pygame.init() 
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Alien Jump') 
clock = pygame.time.Clock() #Frame rate
font = pygame.font.Font('Pixeltype.ttf',64)
game_active = False
start_time = 0
score = 0

background_music = pygame.mixer.Sound('Audio/music.wav')
background_music.set_volume(0.2)
background_music.play(-1)

#Player group
player = pygame.sprite.GroupSingle()
player.add(Player())

#Obstacle Group
obstacle_group = pygame.sprite.Group()


sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()


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

    for event in pygame.event.get(): #check inputs
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #Safe way to completely exit all code
        
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:    
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail', 'snail', 'snail'])))

                     
    if game_active:
        #draw elements
        #update everything

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collision
        game_active = collision_sprite()

    

    else:
        screen.fill('#ADD8E6')
        screen.blit(player_stand,player_stand_rect)

        score_message = font.render(f'Score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,360))

        screen.blit(title_surface,title_rect)

        if score == 0: screen.blit(instruct_surf,instruct_rect)
        else: screen.blit(score_message,score_message_rect)


    pygame.display.update()
    clock.tick(60) #60 times per second: frame rate