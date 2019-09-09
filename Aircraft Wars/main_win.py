# code by pangyusang in 2019.08.14

import pygame
from pygame.locals import *
from numpy import random
from sys import exit
# 定义窗口尺寸大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):

        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.bullets = pygame.sprite.Group()
        self.image_index = 0
        self.speed = 6
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midbottom)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

# 初始化
pygame.init()
# 窗体大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 名称
pygame.display.set_caption("飞机大战")
# icon图标
# ic_launcher = pygame.image.load("")
# pygame.display.set_icon(ic_launcher)
# 背景图片
background = pygame.image.load("resources/image/background.png")
# 游戏结束
gameover = pygame.image.load("resources/image/gameover.png")
# 子弹、玩家、敌机图片
plane_image = pygame.image.load("resources/image/shoot.png")

def startGame():
    # 创建飞机对象
    player_rect = []      # 创建飞机图片集合
    player_rect.append(pygame.Rect(1, 99, 100, 120))
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    # 爆炸飞机
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_image, player_rect, player_pos)
    # 子弹
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_image.subsurface(bullet_rect)

    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_image.subsurface(enemy1_rect)
    enemy1_down_ims = []
    enemy1_down_ims.append(plane_image.subsurface(pygame.Rect(267, 347, 57, 51)))
    enemy1_down_ims.append(plane_image.subsurface(pygame.Rect(873, 697, 57, 51)))
    enemy1_down_ims.append(plane_image.subsurface(pygame.Rect(267, 296, 57, 51)))
    enemy1_down_ims.append(plane_image.subsurface(pygame.Rect(930, 697, 57, 51)))

    enemy_frequency = 0
    shoot_frequency = 0
    player_down_index = 16
    score = 0
    clock = pygame.time.Clock()

    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()
    # 游戏主循环
    running = True
    while running:
        screen.fill(0)
        screen.blit(background, (0, 0))
        clock.tick(60)

        # 子弹
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency +=1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        player.bullets.draw(screen)
        # 敌机
        if enemy_frequency % 50 ==0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_ims, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency +=1
        if enemy_frequency >= 100:
            enemy_frequency = 0

        for enemy in enemies1:
            enemy.move()
            if enemy.rect.top < 0:
                enemies1.remove(enemy)
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break

        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        for enemy_down in enemies_down:
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 1
                # print("Shut down")
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1

        # 玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.image_index], player.rect)
            player.image_index = shoot_frequency //8
        else:
            player.image_index = player_down_index//8
            screen.blit(player.image[player.image_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False


        enemies1.draw(screen)
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        screen.blit(score_text, text_rect)

        # 用户交互
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    screen.blit(gameover, (0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render("Score:" + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery+24
    screen.blit(text, text_rect)
    # 重新开始
    xtfont = pygame.font.SysFont("SimHei", 30)
    textstart = xtfont.render("重新开始", True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery+120
    screen.blit(textstart, text_rect)

startGame()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= screen.get_rect().centerx - 70 \
                    and event.pos[0] <= screen.get_rect().centerx + 50 \
                    and event.pos[1] >= screen.get_rect().centery + 120\
                    and event.pos[1] <= screen.get_rect().centery + 160:
                startGame()

    pygame.display.update()