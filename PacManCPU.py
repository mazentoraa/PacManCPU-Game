import pygame
from pygame.locals import*
from pygame import mixer
import os

#os.chdir(r'C:\Users\LENOVO\Documents\Python\Games\PacManCPU')

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PacManCPU')

#define font
font_score = pygame.font.SysFont('Bauhaus 93', 30)
#define colors
white = (255, 255, 255)
yellow = (255,191,0)

#define game variables
tile_size = 50
blob_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
game_over = 0
score = 0

#load images
bg_img = pygame.image.load(r'img\bg.jpg')
restart_img = pygame.image.load(r'img\Restart.jpg')
restart_image = pygame.transform.scale(restart_img, (400,269))
youwin_img = pygame.image.load(r'img\YouWin.jpg')
youwin_image = pygame.transform.scale(youwin_img, (400,400))

#load sounds
coin_fx = pygame.mixer.Sound(r'img\CoinSound.mp3')
coin_fx.set_volume(0.7)
game_over_fx = pygame.mixer.Sound(r'img\GameoverSound.wav')
game_over_fx.set_volume(0.5)
finish_fx = pygame.mixer.Sound(r'img\finishSound.wav')
finish_fx.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and clicked conditions 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        cooldown = 10

        if game_over == 0:
            #keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.direction = -1
                dx -= 4
            elif key[pygame.K_RIGHT]:
                self.direction = 1
                dx += 4
            elif key[pygame.K_UP]:
                self.direction = 2
                dy -= 4
            elif key[pygame.K_DOWN]:
                self.direction = -2
                dy += 4

            #Check for collision
            for tile in world.tile_list: 
                #Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height)==1:
                    dx = 0
                #Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height)==1:
                    dy = 0
            
            #Check for collision with ennemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                pygame.mixer.music.stop()
                game_over_fx.play()
            
            #handle animation
            self.counter += 1
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 2:
                    self.image = self.images_up[self.index]
                if self.direction == -2:
                    self.image = self.images_down[self.index]
            
            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            #WIN
            if self.rect.x > 600 and self.rect.y == 50:
                game_over = 1
                pygame.mixer.music.stop()
                finish_fx.play()
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 8:
                self.rect.y -= 1
        #draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over
    
    def reset(self, x, y):
        pygame.mixer.music.load(r'img\BgMusic.wav')
        pygame.mixer.music.play(-1, 0.5, 5000)
        coin_group.empty()
        blob_group.empty()
        world = World(world_data)
        self.images_right = []
        self.images_left = []
        self.images_up = []
        self.images_down = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(fr'img\Player{num}1.png')
            img_right = pygame.transform.scale(img_right, (45,45))
            img_left = pygame.image.load(fr'img\Player{num}3.png')
            img_left = pygame.transform.scale(img_left, (45,45))
            img_up = pygame.image.load(fr'img\Player{num}4.png')
            img_up = pygame.transform.scale(img_up, (45,45))
            img_down = pygame.image.load(fr'img\Player{num}2.png')
            img_down = pygame.transform.scale(img_down, (45,45))
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.images_up.append(img_up)
            self.images_down.append(img_down)
        self.image = self.images_down[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = -2
        dead_img = pygame.image.load(r'img\DeadPlayer.png')
        self.dead_image = pygame.transform.scale(dead_img, (45,45))

class World():
    def __init__(self,data):
        self.tile_list = []

        #load images
        bloc_img = pygame.image.load(r'img\Bloc.jpg')
        finish_img = pygame.image.load(r'img\Finish.jpg')
        light_img = pygame.image.load(r'img\Light.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(bloc_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                if tile == 3:
                    img = pygame.transform.scale(finish_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                if tile == 4:
                    blob = Enemy(col_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
                if tile == 5:
                    img = pygame.transform.scale(light_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                if tile == 6:
                    coin = Coin(col_count * tile_size + 25, row_count * tile_size + 20)
                    coin_group.add(coin)
                tile = (img, img_rect)
                self.tile_list.append(tile)
                col_count += 1 
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r'img\Enemy.png')
        self.image = pygame.transform.scale(img, (45,45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 100:
            self.move_direction *= -1
            self.move_counter *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r'img\Logo.png')
        self.image = pygame.transform.scale(img, (25,25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (0, 0, 255), (0, line * tile_size), (SCREEN_WIDTH, line * tile_size))
        pygame.draw.line(screen, (0, 0, 255), (line * tile_size, 0), (line * tile_size, SCREEN_HEIGHT))        

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 6, 6, 6, 0, 1, 6, 6, 6, 6, 6, 3],
[1, 6, 1, 6, 1, 1, 0, 1, 6, 1, 0, 1, 1, 1],
[1, 6, 1, 6, 1, 6, 4, 1, 1, 1, 0, 0, 6, 1],
[1, 6, 1, 6, 1, 0, 0, 6, 6, 6, 1, 0, 0, 1],
[1, 6, 6, 6, 1, 6, 0, 6, 1, 6, 1, 4, 6, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 0, 1, 1],
[1, 0, 0, 5, 6, 6, 6, 6, 6, 6, 1, 0, 6, 1],
[1, 6, 1, 1, 0, 1, 1, 1, 5, 1, 0, 1, 6, 1],
[1, 6, 1, 6, 0, 1, 0, 1, 6, 1, 0, 1, 6, 1],
[1, 6, 1, 0, 4, 1, 1, 1, 6, 1, 0, 1, 6, 1],
[1, 6, 1, 1, 0, 1, 6, 0, 6, 1, 1, 1, 6, 1],
[1, 6, 6, 6, 0, 6, 6, 0, 0, 6, 6, 6, 6, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)
player = Player(50, 50)

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2 )
coin_group.add(score_coin)

#create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, restart_image )
youwin_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200, youwin_image )

run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))
    world.draw()
    coin_group.draw(screen)
    if game_over == 0:
        blob_group.update()

        #update score
        #check if a coin has been collected
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
            coin_fx.play()
        draw_text(' X ' + str(score), font_score, white, tile_size - 10, 10)
    
    blob_group.draw(screen)

    game_over = player.update(game_over)
    #if player has died
    if game_over == -1:
        if restart_button.draw():
            player.reset(50, 50)
            coin_group.add(score_coin)
            game_over = 0
            score = 0

    #WIN
    if game_over == 1:
        if youwin_button.draw():
            finish_fx.stop()
            player.reset(50, 50)
            coin_group.add(score_coin)
            game_over = 0
            score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()

pygame.quit()