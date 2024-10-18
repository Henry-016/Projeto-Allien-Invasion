# Bibliotecas:

import sys
import pygame
import time
from bullet import Bullet
from alien import Alien
from time import sleep

# Funções:


def check_keydown_events(event, ai_settings, screen, ship, bullet, stats):
    """Responde o Pressionamento de Teclas"""

    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullet)
        shoot_ship = pygame.mixer.Sound('sounds/tiro_da_nave.wav')
        shoot_ship.set_volume(0.15)
        shoot_ship.play()
    elif event.key == pygame.K_q:
        stats.save_high_score()
        sys.exit()


def check_keyup_events(event, ship):
    """Responde a "soltura" da tecla"""

    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a Eventos ao Pressionar Teclas ou o Mouse"""

    for event in pygame.event.get():

        # Fecha o Jogo

        if event.type == pygame.QUIT:
            sys.exit()

        # Move a Nave para a Direita ou Esquerda

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)

        # Regula o Movimento da Nave pra Direita ou Esquerda ao Segurar a Tecla (FAZ PARAR)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # Verificando o Botão Play

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um Novo Jogo quando o Jogador Clicar no Play"""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:

        # Oculta o Cursor do Jogo

        pygame.mouse.set_visible(False)

        # Reseta os Dados Estatísticos do Jogo

        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

        # Reinicia as Imagens do Painel de Pontuação

        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()

        # Esvazia a Lista de Aliens e Projéteis

        aliens.empty()
        bullets.empty()

        # Cria uma Nova Frota e Centraliza a Nave

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


# Caminho relativo à localização do arquivo .py ou .exe


# Exemplo de uso
background_image_path = 'images/background_space3.bmp'

background = pygame.image.load(background_image_path)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Atualiza a Tela a todo momento"""

    # Redesenha a Tela:

    screen.blit(background, (0, 0))

    # Redesenha Todos os Projéteis atrás da Nave e dos Aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Desenha a Informação sobre Pontuação

    sb.show_score()

    # Desenha o Botão Play se o Jogo estiver Off

    if not stats.game_active:
        play_button.draw_button()

    # Atualiza a Tela Constantemente

    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza a Posição dos Projetéis e se Libra dos Projetéis Antigos"""

    # Atualiza a Posição dos Projetéis

    bullets.update()

    # Livra-se dos Projéteis que Passam da Tela

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, ship, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, ship, bullets):
    """Responde a Colisão entre Projéteis e Aliens"""

    # Verifica se Houve Colisão

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Se Toda Frota for Destruída, Inicia um Novo Nível

        bullets.empty()
        ai_settings.increase_speed()

        # Aumenta o Nível
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        enemy_death = pygame.mixer.Sound('sounds/Destruiu_nave_inimiga.wav')
        enemy_death.set_volume(0.15)
        enemy_death.play()


last_shot_time = 0  # Tempo do último disparo


def fire_bullet(ai_settings, screen, ship, bullets):
    """Cria um Novo Projétil e o Adiciona ao Grupo de Projéteis"""

    global last_shot_time

    cooldown = 0.1
    current_time = time.time()

    # Verifique se o tempo decorrido é maior que o cooldown

    if current_time - last_shot_time > cooldown:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

        # Atualiza o tempo do último disparo

        last_shot_time = current_time


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o Número de Linhas com Aliens que Cabem na Tela"""

    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def get_number_aliens_x(ai_settings, alien_width):
    """Determina o Número de Aliens que Cabem na Tela"""

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria o Alien e o Posiciona na Linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma Frota Completa de Aliens"""

    # Cria um Alien e Calcula o Número de Aliens em uma Linha
    # O Espaçamento entre os Aliens é igual a Largura de um Alien

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Cria a Primeira Linha de Aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """Faz toda a Frota Descer e Mudar sua Direção"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Responde Apropriadamente se algum Alien Alcançou a Borda da Tela"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde ao Fato da Nave ter sido Atingida por um Alien"""

    if stats.ships_left > 0:

        # Decrementa ships_left

        stats.ships_left -= 1

        # Toca o Som de Destruição

        ship_death = pygame.mixer.Sound('sounds/Destruiu_nave_inimiga.wav')
        ship_death.set_volume(0.15)
        ship_death.play()

        sleep(1)

        # Atualiza o Painel de Pontuações

        sb.prep_ships()

        # Esvazia a Lista de Aliens e Projéteis

        aliens.empty()
        bullets.empty()

        # Cria uma Nova Frota e Centraliza a Nave

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma Pausa

        sleep(0.5)

    else:

        stats.save_high_score()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum Alien Alcançou a Parte Inferior da Tela"""

    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esse caso do mesmo Modo que é feito quando a Nave é atingida
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se a Frota está em uma das Bordas e então Atualiza as Posições de todos os Aliens da Frota"""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifica se Houve Colisão entre os Aliens e a Nave

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Verifica se algum Alien Atingiu a Parte Inferior da Tela

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Verifica se há uma Nova Pontuação Máxima"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
