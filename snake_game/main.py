import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('snake_game/chick.png')
        self.image=pygame.transform.scale(self.image, (50,50))
        self.rect=self.image.get_rect()
        self.rect=self.rect.inflate(-20,-20)
        print("플레이어: ",self.rect)
        self.rect.center=(540,390)
    
    def move(self):
        prssdKeys=pygame.key.get_pressed()
        if self.rect.left>0:
            if prssdKeys[K_LEFT]:
                self.rect.move_ip(-5,0)
                position_p=self.rect.center
                return position_p
        if self.rect.right<640:
            if prssdKeys[K_RIGHT]:
                self.rect.move_ip(5,0)
                position_p=self.rect.center
                return position_p

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('snake_game/boom2.png')
        self.image=pygame.transform.scale(self.image, (50,50))
        self.rect=self.image.get_rect()
        self.rect=self.rect.inflate(-20,-20)
        print("적: ",self.rect)
        self.rect.center=(random.randint(40,600),0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if(self.rect.bottom>440):
            SCORE+=1
            self.rect.top=0
            self.rect.center=(random.randint(30,610),0)
        return self.rect.center

# 초당 프레임 설정
FPS = 60
FramePerSec = pygame.time.Clock()

# 색상 세팅(RGB코드)
RED = (255, 0, 0)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SEAGREEN = (60, 179, 113)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (204, 153, 255)
PINK = (255, 153, 153)

# 게임 진행에 필요한 변수들 설정
SPEED = 5  # 게임 진행 속도
SCORE = 0  # 플레이어 점수

# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("GG", True, BLACK)  # 게임 종료시 문구

# 게임 배경화면
background = pygame.image.load('snake_game/background1.jpg')  # 배경화면 사진 로드
background=pygame.transform.scale(background, (640,440))

# 게임 화면 생성 및 설정
GameDisplay = pygame.display.set_mode((640, 440))
GameDisplay.fill(PINK)
pygame.display.set_caption("Mini Game")

P=Player()
E=Enemy()

Enemies=pygame.sprite.Group()
Enemies.add(E)

All_groups=pygame.sprite.Group()
All_groups.add(P)
All_groups.add(E)

increaseSpeed=pygame.USEREVENT+1
pygame.time.set_timer(increaseSpeed,1000)


while True:

    for event in pygame.event.get():
        if event.type==increaseSpeed:
            SPEED+=0.5
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    GameDisplay.blit(background,(0,0))
    scores=small_font.render("Score: "+str(SCORE),True,BLACK)
    GameDisplay.blit(scores,(10,400))

    for i in All_groups:
        GameDisplay.blit(i.image,i.rect)
        i.move()
        if str(i)=='<Player Sprite(in 1 groups)>':
            player_pos=i
        else:
            enemy_pos=i
    
    if pygame.sprite.spritecollideany(P,Enemies):
        for i in All_groups:
            i.kill()
        GameDisplay.blit(background,(0,0))
        image0=pygame.image.load('snake_game/chickbommed.png')
        image0=pygame.transform.scale(image0, (50,50))
        image0.get_rect()
        GameDisplay.blit(image0, player_pos)

        image1=pygame.image.load('snake_game/boomm.png')
        image1=pygame.transform.scale(image1, (50,50))
        image1.get_rect()
        GameDisplay.blit(image1,enemy_pos)
        pygame.display.update()

        GameDisplay.fill(SEAGREEN)
        final_scores=font.render("Your Score: "+str(SCORE),True,BLACK)
        GameDisplay.blit(final_scores,(150,100))
        GameDisplay.blit(game_over,(280,200))
        time.sleep(1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)