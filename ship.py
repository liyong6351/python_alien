import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship,self).__init__()
        self.settings = ai_settings
        self.screen = screen

        self.image=pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        # 在飞船的属性中存储小数值
        self.center = float(self.rect.centerx)


    def blitme(self):
        self.screen.blit(self.image,self.rect)

    # 持续移动
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect.centerx += 1
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            #self.rect.centerx -= 1
            self.center -= self.settings.ship_speed_factor
        self.rect.centerx = self.center

    # 将飞船在屏幕上居中
    def center_ship(self):
        self.center = self.screen_rect.centerx