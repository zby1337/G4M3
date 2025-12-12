
import pygame
import os

pygame.init()

screen_width = 1000
screen_height = int(screen_width * 0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Крутые реперы 90ых против тупых опиумных нигеров соверемнности')

#установка частоты кадров
clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75


moving_left = False
moving_right = False


#определение цвета
BG = (255,	192,	203)
RED = (255, 255, 0)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 300), (screen_height, 300))


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
				img = pygame.image.load(f'E:/CreateG4ME/DAAAAMN sprites/{self.char_type}/{animation}/{i}.png')
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


player = warrior('player', 300, 200, 3, 5)
enemy = warrior('enemy', 500, 200, 3, 5)

#запуск игры
run = True

while run:

	clock.tick(FPS)

	draw_bg()  # очистка фона


	player.update_animation()
	enemy.update_animation()
	player.draw()
	enemy.draw()


	#обновляем действие
	if player.alive:
		if player.in_air:
			player.update_action(2) #2 - прыгать
		elif moving_left or moving_right:
			player.update_action(1) #1 - бежать
		else:
			player.update_action(0) #0 - стоять

	player.move(moving_left, moving_right)

	for event in pygame.event.get():
		#выход из игры
		if event.type == pygame.QUIT:
			run = False

		#нажатия на клавиши
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a: #ходьба влево
				moving_left = True
			if event.key == pygame.K_d: #ходьба вправо
				moving_right = True
			if event.key == pygame.K_w and player.alive: # прыжок
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False

		#отжатие клавиши
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False


	pygame.display.update()		

pygame.quit()


