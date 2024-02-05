import pygame
import pygame.font as font

class Button():
	
	def __init__(self, ai_game, message):
		#атрибуты кнопки
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		
		# размеры кнопки
		
		self.width, self.height = 200, 50
		self.button_color = (0, 140, 0)
		self.text_color = [255, 255, 255]
		self.font = font.SysFont(None, 40)
		
		# добавление кнопки и выравнивание
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
		self._p_message(message)
		
		
	def _p_message(self,message):
		# риусет текст в прямоугольнике
		self.message_image = self.font.render(
			message, True, self.text_color, self.button_color) # преобразует шрифт в картинку
		# Т - режим сглаживания
		self.message_image_rect = self.message_image.get_rect()
		self.message_image_rect.center = self.rect.center
		
	def draw_button(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.message_image, self.message_image_rect)
		
class New_Button (Button):
	
	def __init__(self,ai_game, message, xy , color , size, font_syze):
		super(New_Button, self).__init__(ai_game, message)
		# атрибуты кнопки
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		
		# размеры кнопки
		
		self.width, self.height = size[0],size[1]
		self.button_color = color
		self.text_color = [255, 255, 255]
		self.font = font.SysFont(None, font_syze)
		
		# добавление кнопки и выравнивание
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = xy[0]
		self.rect.centery = xy[1]
		self._p_message(message)
		