# -*- coding: UTF-8 -*-

import pygame.font
from pygame.sprite import Group
from ship import Ship

# 显示得分信息的类
class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始化得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    # 将得分放在屏幕右上角
    def prep_score(self):
        round_score = int(round(self.stats.score,-1))
        score_str = "current:" + "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_rect.right
        self.score_rect.top = 20

    # 渲染最高得分
    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str =  "highest:" + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.score_rect.right + 100
        self.high_score_rect.top = self.score_rect.top

    # 将等级渲染为图像
    def prep_level(self):
        self.level_image = self.font.render( "level:" + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        # 将等级显示在最下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width + 500
            ship.rect.y = 10
            self.ships.add(ship)

    # 显示得分
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect) 
        self.ships.draw(self.screen)       