# Создадим класс для окна в pygame

import sys
from time import sleep
import pygame as py
from settings import Settings
from game_stat import stat
from ship import Ship
from bullet import Bullet
from Button import Button, New_Button
from Alien import Alien
from Scoreboard import Scoreboard
import shelve
class AlienInvasion():
	
	def __init__(self):
		# инициализирует работу класса
		py.init()
		self.settings=Settings()
		self.stat = stat(self)
		# размер экрана из настроек и настройка самого экрана
		self.screen = py.display.set_mode((0, 0), py.FULLSCREEN)
		self.buff_wigth = self.settings.screen_width
		self.buff_heigth = self.settings.screen_height
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		py.display.set_caption("Alien Invasion")
		# Прописовка корабля
		self.ship = Ship(self)
		self.bullets = py.sprite.Group()
		self.aliens = py.sprite.Group()
		self._create_fleet()
		self.play_button = Button(self, "Играть")
		self.play_mode_button = New_Button(self, 'Уровень сложности',
		                                   (960,640), [140,0,0], (300, 50), 35)
		self.hard_button=New_Button(self, 'Сложно',
		                                   (960,440), [140,0,0], (300, 50), 35)
		self.medium_button=New_Button(self, 'Нормально',
		                                   (960,540), [255,222,0], (300, 50), 35)
		self.easy_button=New_Button(self, 'Просто',
		                                   (960,640), [0,140,0], (300, 50), 35)
		self.SB = Scoreboard(self)
		
		
	
	def run_game(self):
		# начинает игру
		while True:
			#Отслеживает события на клавиатуре и мышке
			self._check_ivents()  # проверка на ивенты
			if self.stat.game_active: # если игра активна
				self.ship.Update() # обновляет положение корабля
				self.update_bullets()#обновляет положение пули
				self._update_aliens() # урпавляет флотом пришельцев
			self._update_screen() #при каждом проходе цикла прописовывается экран

			
	def _check_ivents(self):   #вспомогательный класс для run game
		# ждёт нажатия клавиш и события мышки
		for event in py.event.get():
			if event.type == py.QUIT:
				sys.exit()
			elif event.type == py.KEYDOWN:
				self._check_keydown(event)   # события для нажатой клавиши
			elif event.type == py.KEYUP:
				self._check_keyup(event)  # события для отпущенной клавиши
			elif event.type == py.MOUSEBUTTONDOWN:  # нажатие на кнопку плэй
				mouse_pos = py.mouse.get_pos()
				self._check_button(mouse_pos)
				
	def _check_keydown(self,event):    # вспомогательный для check_ivents
		# для ивентов нажатой клавиши
		if event.key == py.K_d:  # вправо
			self.ship.moving_right = True
		elif event.key == py.K_a: # влево
			self.ship.moving_left = True
		elif event.key == py.K_ESCAPE: # выход
			sys.exit()
		elif event.key == py.K_o: # смена разрешения экрана
			self.switch_fullscreen()
		elif event.key == py.K_SPACE: # стрельба
			self._fire_bullet()
		elif event.key == py.K_p and not self.stat.game_active:
			self._start_game()
		
			
	def _check_button(self,mouse_pos):
		# новая игра при нажатии Play
		button_click_play = self.play_button.rect.collidepoint(mouse_pos)
		button_click_mode = self.play_mode_button.rect.collidepoint(mouse_pos)
		button_hard = self.hard_button.rect.collidepoint(mouse_pos)
		button_easy = self.easy_button.rect.collidepoint(mouse_pos)
		if button_click_play and not self.stat.game_active:
			self.stat.mode = 'normal'
			self.settings.alien_speed = 3.0
			self.settings.fleet_drop = 10
			self.settings.bullets_allowed = 6
			self._start_game()
			self.SB.prep_score()
			self.SB.prep_level()
			self.SB.prep_ships()
		elif button_click_mode and not self.stat.game_mode and not self.stat.game_active:
			self.stat.reset_stat()
			self.stat.game_mode=True
		elif button_hard and self.stat.game_mode:
			self.settings.alien_speed = 5.0
			self.settings.fleet_drop = 11
			self.settings.bullets_allowed=8
			self.stat.mode='hard'
			self._start_game()
		elif button_easy and self.stat.game_mode:
			self.settings.alien_speed = 1.0
			self.settings.fleet_drop = 5
			self.settings.bullets_allowed = 13
			self.stat.mode = 'easy'
			self._start_game()
			

	def _start_game(self):
		self.settings.initialize_dynamic_set()
		self.aliens.empty()
		self.bullets.empty()
		self.stat.game_active = True
		self.stat.game_mode = False
		self._create_fleet()
		self.ship.center_ship()
		self.stat.get_pay_points()
	
		py.mouse.set_visible(False)
	
	
	
	def _check_keyup(self,event):  # вспомогательный для check_ivents
		# для ивентов отпущенной клавиши
		if event.key == py.K_d:
			self.ship.moving_right = False
		elif event.key == py.K_a:
			self.ship.moving_left = False
			
			
	def _update_screen(self): #вспомогательный класс для run game
		# обновляет экран
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites(): # рисуем пули
			bullet.draw_bullet()
		self.aliens.draw(self.screen) # рисуем пришельцев
		self.SB.show_score()
		if not self.stat.game_mode and not self.stat.game_active:  # метод для кнопки
			self.play_button.draw_button()
			self.play_mode_button.draw_button()
		elif self.stat.game_mode and not self.stat.game_active:
			self.hard_button.draw_button()
			self.medium_button.draw_button()
			self.easy_button.draw_button()
		# последний прорисованный экран
		py.display.flip()
		
	
	def switch_fullscreen(self):
		# поменять размер экрана (пока так себе)
		if py.display.get_window_size() == (self.buff_wigth,self.buff_heigth):
			# полноэкранный режим
			self.screen = py.display.set_mode((0, 0), py.FULLSCREEN)
			self.settings.screen_width = self.screen.get_rect().width
			self.settings.screen_height = self.screen.get_rect().height
			
			self.ship.rect.midbottom = self.screen.get_rect().midbottom
		else:
			self.settings.screen_width = self.buff_wigth
			self.settings.screen_height = self.buff_heigth
			self.screen = py.display.set_mode((self.settings.screen_width, self.settings.screen_height))
			self.ship.rect.midbottom = self.screen.get_rect().midbottom
		self._update_screen()


	def update_bullets(self):
		# передвижение пули, удаление на маркерах, проверка попадания в пришельцев
		self.bullets.update()
		self._del_bullets()
		# проверика попадания в пришельцев и их уничтожение
		self._check_bullet_alien_collide()
		
	def _check_bullet_alien_collide(self):
		# проверка на соприкосновение пули и пришельца, при совпадении удаление и того и другого
		# при уничтожении всех врагов удаление пуль с экрана и создание нового флота
		collisions = py.sprite.groupcollide(
			self.bullets, self.aliens, True, True)
		if collisions:
			self.stat.score += self.settings.alien_points
			self.SB.prep_score()
			self.check_high_score()
		# первый Т показывает надо ли уничтожать пулю, второй-пришельца
		if not self.aliens:
			# удаление существующих снарядов и добавление нового флота
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			if self.stat.mode == 'hard':
				self.settings.alien_points += 80
			elif self.stat.mode == 'normal':
				self.settings.alien_points += 30
			elif self.stat.mode == 'easy':
				self.settings.alien_points += 15
			self.stat.level += 1
			self.SB.prep_level()
			self.settings.increase_speed()
	
	def check_high_score(self):
		if self.stat.score > self.stat.high_score:
			self.stat.high_score = self.stat.score
			self.SB.prep_high_score()
			
	
	def _fire_bullet(self):
		# создаю новый снаряд
		if len(self.bullets) < self.settings.bullets_allowed:  # ограниченное кол-во зарядов
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	
	def _del_bullets(self):
		# при достижении маркера удаляет пулю
		for bullet in self.bullets.copy():  # copy для того, чтобы можно было изменять bullets
			if bullet.rect.bottom <=0:
				self.bullets.remove(bullet)
				
	def _create_fleet(self):
		# создание флота
		# создаём пришельца и вычислим количество пришельцев в ряду
		#интервал между пришельцами равен одному пришельцу
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		num_aliens_x = available_space_x // (2 * alien_width)
		
		# определим количество рядов на экране
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (7 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)
		
		# Создадим первый ряд пришельцев
		for row_num in range(number_rows):
			for alien_num in range(num_aliens_x):
				self._create_alien(alien_num , row_num)
				
	def _create_alien(self, alien_num, row_num):
		# создание рядов и столбцов из пришельцев
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x= alien_width + 2 * alien_width * alien_num
		alien.y= alien_height + 2 * alien_height * row_num
		alien.rect.x = alien_width + 2 * alien_width * alien_num
		alien.rect.y = alien_height + 2 * alien_height * row_num
		self.aliens.add(alien)
		
	
	def _update_aliens(self):
		# проверка у стены ли пришелец, передвижение, получение урона и достижение врагами низа экрана
		self._check_fleet_edges()
		self.aliens.update()
		# колизия пришелец - корабль
		if py.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		self._check_aliens_bottom()
		
			
	def _ship_hit(self):
		# если корабль получает урон или пришельцы доходят до низа экрана
		# жизни уменьшаются и создаётся новый флот и обновляется положение корабля
		if self.stat.ships_left > 0:
			self.stat.ships_left -= 1
			self.SB.prep_ships()
			#очистка
			self.aliens.empty()
			self.bullets.empty()
			#новый флот
			self._create_fleet()
			self.ship.center_ship()
			# небольшая пауза
			sleep(0.5)
		else:
			self.stat.game_active = False
			self.stat.game_mode = False
			self.stat.reset_stat()
			self.SB.show_score()
			self.sefe_my_record()
			py.mouse.set_visible(True)

		
	def sefe_my_record(self):
		shelfFile = shelve.open('data')
		shelfFile['High_score'] = self.stat.high_score
		shelfFile.close()
		
	def _check_aliens_bottom(self):
		# добрались ли пришельцы до низа экрана
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break
				
	def _check_fleet_edges(self):
		# если пришельцы добрались до стены, мнеяют направление и спускаются вниз
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
		
	
	def _change_fleet_direction(self):
		# спуск пришельцев вниз и поворот в обратную сторону
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop
		self.settings.fleet_direction *= -1
	

		

if __name__ == '__main__':
	# создать экземпляр
	ai=AlienInvasion()
	ai.run_game()
	