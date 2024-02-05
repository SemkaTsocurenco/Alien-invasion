import pygame as py
from PIL import Image
import os
from settings import Settings
from pygame.sprite import Sprite
class Ship(Sprite):
	# управление кораблём
	def __init__(self,ai_game):
		super().__init__()
		self.screen = ai_game.screen   # получаем экземпляр экрана
		self.settings = ai_game.settings # получаем настройки

		self.screen_rect = ai_game.screen.get_rect() # получение коорд экрана
		
		#Загрузим изображение корабля
		self.image = py.image.load(
			".\\images\\new_space_ship.png")
		self.rect = self.image.get_rect() # координаты корабля
		# Появление корабля снизу экрана
		self.rect.midbottom = self.screen_rect.midbottom # снизу по центру
		
		# Сохраняем вещественную координату центра корабля
		self.x = float(self.rect.x)
		
		#для переещения
		self.moving_right = False
		self.moving_left = False
		
	def blitme(self):
		#корабль в текущей позиции
		self.screen.blit(self.image, self.rect)
	
	def Update(self):
		# обновление позиции
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left>self.screen_rect.left:
			self.x -= self.settings.ship_speed
	
		#обновление rect на основании х
		self.rect.x = self.x
	
	def center_ship(self):
		# корабль по центру
		self.rect.midbottom=self.screen_rect.midbottom
		self.x = float(self.rect.x)
	
	
	
def resize_im(path):
	img=Image.open(path)
	img=img.resize((50,50))
	img.save(f'{os.path.dirname(path)}\\new_{os.path.basename(path)}')
	
resize_im("C:\\Users\\semn-\\PycharmProjects\\AlienIsol\\images\\Alien.png")