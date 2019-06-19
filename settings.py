class Settings():
    # 存储所有设置的类
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        self.ship_speed_factor = 3

        # 子弹的设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 限制子弹数量
        self.bullet_allowed = 30

        #外星人设置
        self.fleet_drop_speed = 50
        

        # 每个玩家拥有的飞船条数
        self.ship_limit = 3
        # 外星人点数的提高速度
        self.score_scale = 1.1

        # 以什么样的速度加快游戏节奏
        self.speed_scale = 1.5
        self.initialized_dynamic_settings()

    # 初始化需要变更的设置
    def initialized_dynamic_settings(self):
        self.ship_speed_factor = 3.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 2
        # 1表示右移，-1表示左移
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    # 提高速度
    def increase_speed(self):
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        # 得分提高
        self.alien_points = int(self.alien_points * self.score_scale)