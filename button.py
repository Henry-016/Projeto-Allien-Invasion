# Bibliotecas

import pygame.font


class Button():
	"""Cria um Botão na Tela"""
	
	def __init__(self, ai_settings, screen, msg):
		"""Inicaliza os Atributos do Botão"""
		
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		# Define as Dimensões do Botão
		
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)
		
		# Cosntrói o Objeto Rect do Botão e o Centraliza na Tela
		
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
		
		# A Mensagem do Botão deve ser Preparada Somente uma Vez
		
		self.prep_msg(msg)
		
	def prep_msg(self, msg):
		"""Transforma msg em Imagem Renderizada e Centraliza o Texto no Botão"""
		
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		"""Desenha um Botão em Branco, e em seguida, Desenha a Mensagem"""
		
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
