import math

class Settings():
	# настройки игры

	def __init__(self):
		# Инициализация настроек игры
		self.screen_width=1200
		self.screen_height=800
		self.bg_color=(230, 230, 230)
		self.ship_speed=6
		self.ship_limit = 3
		#параметры пули
		self.bullet_color=(60, 60, 60)
		self.bullet_speed = 2
		self.bullet_width = 3
		self.bullet_heigth= 15
		self.bullets_allowed =6
		# Настройка пришельцев
		self.alien_speed = 1.5
		self.fleet_drop =10
		self.fleet_direction = 1 # 1 - вправо -1 - влево
		# Темп ускорения
		self.speedup_scale = 1.2
		self.initialize_dynamic_set()
		
	def initialize_dynamic_set(self):
		# изменяемые параметры игры
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 1.5
		self.alien_speed_factor = 1.5
		self.fleet_direction = 1  # 1 - вправо -1 - влево
		self.alien_points = 50
		
	def increase_speed(self):
		# увеличеник скорости игры
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
