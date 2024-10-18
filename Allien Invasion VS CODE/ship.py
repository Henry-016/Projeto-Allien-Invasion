# Bibliotecas

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
	"""Classe para Manipular a Nave do Jogo"""

	def __init__(self, ai_settings, screen):
		"""Inicializa a Nave e Define sua Posição Inicial"""

		super(Ship, self).__init__()

		self.screen = screen
		self.ai_settings = ai_settings

		# Carrega a Imagem da Nave e Obtém seu Rect, além de deixar a Imagem Transparente

		self.image = pygame.image.load('images/ship.bmp').convert_alpha()
		color = self.image.get_at((0, 0))
		self.image.set_colorkey(color)
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Inicia Cada Nave em sua Posição Atual
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# Armazena um Valor Decimal para o Centro da Nave
		self.center = float(self.rect.centerx)

		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Atualiza a Posição da Nave a partir da flag de movimento"""

		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		# Atualiza o Objeto de acordo com o self.center
		self.rect.centerx = self.center

	def blitme(self):
		"""Desenha a Nave em sua Posição Atual"""

		self.screen.blit(self.image, self.rect)
		
	def center_ship(self):
		"""Centraliza a Nave na Tela"""
		
		self.center = self.screen_rect.centerx
