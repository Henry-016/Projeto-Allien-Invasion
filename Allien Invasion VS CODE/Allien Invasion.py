# Bibliotecas

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Inicializa o Jogo e Cria um Objeto pra Tela"""

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Invasão Alien')

    # Cria um Botão Play

    play_button = Button(ai_settings, screen, 'Play')

    # Cria uma Instância para Armazenar Dados Estatísticos e Cria um Painel de Pontuação

    stats = GameStats(ai_settings)

    sb = Scoreboard(ai_settings, screen, stats)

    # Cria uma Nave, um Grupo de Projéteis e um Grupo de Aliens

    ship = Ship(ai_settings, screen)

    bullets = Group()

    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Principal Laço do Jogo:

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()