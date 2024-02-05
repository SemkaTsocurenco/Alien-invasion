import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	# выводим игровую информацию сверху экрана
	def __init__(self,ai_game):
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stat = ai_game.stat
		
		# шрифт
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,40)
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	
	def prep_score(self):
		# шрифт в изображение
		score_str = str(self.stat.score)
		self.score_img = self.font.render(score_str, True
		                                  , self.text_color, self.settings.bg_color)
		#вывод счёта
		self.score_rect = self.score_img.get_rect()
		self.score_rect.right = self.screen_rect.right -20
		self.score_rect.top = 20
		
	def show_score(self):
		self.screen.blit(self.score_img, self.score_rect)
		self.screen.blit (self.high_score_img, self.high_score_rect)
		self.screen.blit (self.lvl_img, self.lvl_rect)
		self.ships.draw(self.screen)
		
	def prep_high_score(self):
		high_score = round(self.stat.high_score, -1)
		high_score_str = '{:,}'.format(high_score)
		self.high_score_img = self.font.render(high_score_str, True,
		                                       self.text_color, self.settings.bg_color)
		
		self.high_score_rect = self.high_score_img.get_rect()
		self.high_score_rect.centerx=self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
	
	def prep_level(self):
		lvl_str = str(self.stat.level)
		self.lvl_img = self.font.render(lvl_str, True
		                                  , self.text_color, self.settings.bg_color)
		# вывод счёта
		self.lvl_rect = self.score_img.get_rect()
		self.lvl_rect.right = self.score_rect.right
		self.lvl_rect.top = self.score_rect.bottom +10
		
	def prep_ships(self):
		self.ships = Group()
		for ship_num in range(self.stat.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_num * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)