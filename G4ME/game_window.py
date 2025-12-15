import pygame
import os

pygame.init()

screen_width = 800
screen_height = int(screen_width * 1)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('БЕЙ БЕГИ')

#установка частоты кадров
clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75 #гравитация

moving_left = False
moving_right = False


#Загрузка изображений
#Пуля
#bullet_img = pygame.image.load('E:/CreateG4ME/DAAAAMN sprites/icons/bullet').convert_alpha()

#определение цвета
BG = (255,	192, 203)
RED = (255, 255, 255)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 300), (screen_height, 300))


#класс кнопка
class Button:
	def __init__(self, x, y, width, height, text):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.font = pygame.font.SysFont('arial', 40)

	def draw(self, surface):
		mouse_pos = pygame.mouse.get_pos()
		color = (200, 100, 150) if self.rect.collidepoint(mouse_pos) else (180, 80, 130)
		pygame.draw.rect(surface, color, self.rect)
		pygame.draw.rect(surface, (0, 0, 0), self.rect, 3)

		text_surf = self.font.render(self.text, True, (0, 0, 0))
		text_rect = text_surf.get_rect(center=self.rect.center)
		surface.blit(text_surf, text_rect)

	def is_clicked(self, event):
		return (
			event.type == pygame.MOUSEBUTTONDOWN
			and event.button == 1
			and self.rect.collidepoint(event.pos)
		)



class warrior(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

		#загрузка всех картинок для игрока
		animation_types = ['Stand', 'Run', 'Jump']
		for animation in animation_types:
			#перезапуск временного списка изображений
			temp_list = []
			#определение числа элементов в папке
			num_of_frames = len(os.listdir(f'E:/CreateG4ME/DAAAAMN sprites/{self.char_type}/{animation}'))
			for i in range (num_of_frames):
				img = pygame.image.load(f'E:/CreateG4ME/DAAAAMN sprites/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (float(img.get_width() * scale), float(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)



	#метод движения
	def	move(self, is_moving_left, is_moving_right, ):

		dx = 0
		dy = 0

		if is_moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1

		if is_moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#прыжок
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		# ГРАВИТАЦИЯ
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		#проверить столкновение с полом
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False

		self.rect.x += dx
		self.rect.y += dy


	def update_animation(self):
		#обновление анимации
		ANIMATION_COOLDOWN = 100
		#обновление зависит от определенного кадра
		self.image = self.animation_list[self.action][self.frame_index]
		#достаточно ли прошло времени с прошлого обновления
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#если индекс вышел за пределы списка анимаций, возвращаемся назад
		if self.frame_index >= len(self.animation_list[self.action]):
			self.frame_index = 0



	def update_action(self, new_action):
		#проверяем отличается ли действие от предыдущего
		if new_action != self.action:
			self.action = new_action
			#обновляем настройки анимации
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


play_button = Button(300, 300, 200, 60, 'ИГРАТЬ')
exit_button = Button(300, 400, 200, 60, 'ВЫХОД')

#класс пули
class Bullet(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		#self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction


#создание группы спрайтов
bullet_group = pygame.sprite.Group()

#персонажи
player = warrior('player', 300, 200, 3, 5)
enemy = warrior('enemy', 500, 200, 3, 5)

game_state = 'menu'
run = True

#запуск игры
while run:
	clock.tick(FPS)

	if game_state == "menu":
		screen.fill(BG)
		play_button.draw(screen)
		exit_button.draw(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if play_button.is_clicked(event):
				game_state = "game"
			if exit_button.is_clicked(event):
				run = False

	elif game_state == "game":
		draw_bg()

		player.update_animation()
		enemy.update_animation()

		player.draw()
		enemy.draw()

		if player.alive:
			if player.in_air:
				player.update_action(2)
			elif moving_left or moving_right:
				player.update_action(1)
			else:
				player.update_action(0)

		player.move(moving_left, moving_right)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					moving_left = True
				if event.key == pygame.K_d:
					moving_right = True
				if event.key == pygame.K_w:
					player.jump = True
				if event.key == pygame.K_ESCAPE:
					game_state = "menu"
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					moving_left = False
				if event.key == pygame.K_d:
					moving_right = False

	pygame.display.update()

pygame.quit()


