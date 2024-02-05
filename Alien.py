import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	
	def __init__(self,ai_game):
		super().__init__()
		self.screen=ai_game.screen
		self.image = pygame.image.load(
			".\\images\\new_alien.png")
		self.rect = self.image.get_rect()
		self.set = ai_game.settings
		
		# каждый новый прешелец появляется в левом верхнем экране
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)
		
		
	def update(self):
		self.x += self.set.alien_speed * self.set.fleet_direction
		self.rect.x = self.x
		

		
	def check_edges(self):
		# True если пришелец у стены
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <=0:
			return True
	
	
		