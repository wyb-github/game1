class Settings():

    #存储《外星人》中所有设置的类
    def __init__(self):
        """初始化游戏的设置"""

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (230,230,230)
        
        #设置飞船
        self.ship_speed_factor = 1.5

        #子弹的设置
        self.bullet_speed_factor = 1
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 10

        #外星人设置
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 10
        #fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
