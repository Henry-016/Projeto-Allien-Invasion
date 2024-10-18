# Bibliotecas

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Classe para Administrar Projéteis Disparados pela Nave"""

    def __init__(self, ai_settings, screen, ship):
        """Cria um Objeto para a Posição Atual da Nave"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Cria um Retângulo para o Projétil em (0, 0) e, em seguida, Define a Posição Correta

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Armazena a Posição em Projétil como um Valor Decimal

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move o Projétil pra Cima da Tela"""

        # Atualiza a Posição do Projétil

        self.y -= self.speed_factor

        # Atualiza a Posição do Rect

        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o Projétil na Tela"""

        pygame.draw.rect(self.screen, self.color, self.rect)
