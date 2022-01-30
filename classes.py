import pygame

SCREEN = WIDTH, HEIGHT = (1200, 400)

class Ground():
	def __init__(self):
		self.image = pygame.image.load('Assets/ground.png')

		self.width = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width
		self.y = 350

	def update(self, speed):
		self.x1 -= speed
		self.x2 -= speed

		if self.x1 <= -self.width:
			self.x1 = self.width

		if self.x2 <= -self.width:
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))

class ReverseGround():
	def __init__(self):
		self.image = pygame.image.load('Assets/ground.png')
		self.image = pygame.transform.flip(self.image, False, True)

		self.width = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width
		self.y = 30

	def update(self, speed):
		self.x1 -= speed
		self.x2 -= speed

		if self.x1 <= -self.width:
			self.x1 = self.width

		if self.x2 <= -self.width:
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))		


class Dino():
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.duck_list = []

		for i in range(1, 4):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			img = pygame.transform.scale(img, (52, 58))
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			img = pygame.transform.scale(img, (70, 38))
			self.duck_list.append(img)

		self.dead_image = pygame.image.load(f'Assets/Dino/8.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (52,58))

		self.reset()

		self.vel = 0
		self.gravity = 1
		self.jumpHeight = 15
		self.isJumping = False

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.bottom = self.base

		self.alive = True
		self.counter = 0
		self.reverse = False

	def updateImage(self, reverse):
		self.run_list = []
		for i in range(1, 4):
			img = pygame.image.load(f'Assets/Dino/{i}.png')
			if reverse:
				img = pygame.transform.flip(img, False, True)
			img = pygame.transform.scale(img, (52, 58))
			self.run_list.append(img)
	
	def update(self, jump, duck, reverse):
		if self.alive:
			if reverse:
				self.counter += 1
				if self.counter >= 4:
					self.index = (self.index + 1) % len(self.run_list)
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = 100
					self.counter = 0
				
			else:	
				if not self.isJumping and jump:
					self.vel = -self.jumpHeight
					self.isJumping = True

				self.vel += self.gravity
				if self.vel >= self.jumpHeight:
					self.vel = self.jumpHeight

				self.rect.y += self.vel
				if self.rect.bottom > self.base:
					self.rect.bottom = self.base
					self.isJumping = False

				if duck:
					self.counter += 1
					if self.counter >= 6:
						self.index = (self.index + 1) % len(self.duck_list)
						self.image = self.duck_list[self.index]
						self.rect = self.image.get_rect()
						self.rect.x = self.x
						self.rect.bottom = self.base
						self.counter = 0

				elif self.isJumping:
					self.index = 0
					self.counter = 0
					self.image = self.run_list[self.index]
				else:
					self.counter += 1
					if self.counter >= 4:
						self.index = (self.index + 1) % len(self.run_list)
						self.image = self.run_list[self.index]
						self.rect = self.image.get_rect()
						self.rect.x = self.x
						self.rect.bottom = self.base
						self.counter = 0

				self.mask = pygame.mask.from_surface(self.image)

		else:
			self.image = self.dead_image

	def draw(self, win):
		win.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super(Obstacle, self).__init__()

		self.image_list = []
		for i in range(5):
			scale = 0.25
			img = pygame.image.load(f'Assets/Obstacle/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 365

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Flying_Obstacle(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Flying_Obstacle, self).__init__()

		self.image_list = []
		for i in range(2):
			scale = 0.05
			img = pygame.image.load(f'Assets/Flying Obstacle/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.counter += 1
			if self.counter >= 6:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)


class Cloud(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Cloud, self).__init__()
		self.image = pygame.image.load(f'Assets/cloud.png')
		self.image = pygame.transform.scale(self.image, (60, 18))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Star(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Star, self).__init__()
		image = pygame.image.load(f'Assets/stars.png')
		self.image_list = []
		for i in range(3):
			img = image.subsurface((0, 20*(i), 18, 18))
			self.image_list.append(img)
		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)