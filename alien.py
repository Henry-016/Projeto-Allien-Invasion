# Bibliotecas

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Uma Classe que Representa um Único Alien da Frota"""

    def __init__(self, ai_settings, screen):
        """Inicializa o Alien e Define sua Posição Inicial"""

        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a Imagem do Alien e Define sei Atributo Rect, além de deixar a Imagem Transparente

        self.image = pygame.image.load('images/alien.bmp').convert_alpha()
        color = self.image.get_at((0, 0))
        self.image.set_colorkey(color)
        self.rect = self.image.get_rect()

        # Inicia cada Novo Alien Próximo a parte Superior Esquerda da Tela

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a Posição Exata do Alien

        self.x = float(self.rect.x)

    def blitme(self):
        """Desenha o Alien em sua Posição Atual"""

        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Retorna TRUE se o Alien Bater na Borda da Tela"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move o Alien para a Direita e Esquerda"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
