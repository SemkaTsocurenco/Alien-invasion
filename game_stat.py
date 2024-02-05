import pygame
import shelve


class stat():
	
	def __init__(self,ai_game):
		self.game_active = False
		self.set = ai_game.settings
		self.reset_stat()
		self.game_mode = False
		self.mode = 'normal'
		shelFile = shelve.open('data')
		self.high_score=shelFile['High_score']
		shelFile.close()
		
		
	def reset_stat(self):
		# инициализация статистки
		self.ships_left = self.set.ship_limit
		self.score = 0
		self.level = 1
		
		
	def get_pay_points(self):
		if self.mode == 'hard':
			self.set.alien_points = 100
		if self.mode == 'normal':
			self.set.alien_points = 50
		if self.mode == 'easy':
			self.set.alien_points = 35
		
