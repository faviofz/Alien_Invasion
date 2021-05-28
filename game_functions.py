import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Atento a los eventos de ratón y teclado.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_buttton(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Redibuja la pantalla en cada iteracion del bucle.
    screen.fill(ai_settings.bg_color)

    # Redibuja todas las municiones entre la nave y los aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    # Hace visible la pantalla dibujada más reciente.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Actualiza la posicion de las municiones.
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Checkea cualquier municion que haya golpeado un alien.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Creamos un nuevo objeto Bullet y lo agregamos al grupo de bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):  # Crea una flota completa de aliens
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Crea la flota de aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # Determina el numero de aliens que entran en una fila.
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Crea un alien y lo coloca en la fila.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    # Determina el numero de filas de aliens que entran en la pantalla.
    avaliable_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Busca colision de un alien con la nave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Busca aliens que alcancen la parte inferior de la pantalla
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destruye las municiones existentes y crea una nueva flota.
        bullets.empty()
        ai_settings.increase_speed()

        # Incrementa de nivel
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Responde a la nave siendo golpeada por un alien.
    if stats.ships_left > 0:
        # Decrementa las naves restantes.
        stats.ships_left -= 1

        # Actualiza el tablero de puntaje
        sb.prep_ships()

        # Vacia la lista de aliens y municiones.
        aliens.empty()
        bullets.empty()

        # Crea una nueva flota y centra la nave.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pausa
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Chequea si algun alien alcanza la parte inferior de la pantalla.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Realiza la misma acción como si la nave fuera derribada.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_play_buttton(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()

        pygame.mouse.set_visible(False)
        # Reinicia las estadisticas del juego
        stats.reset_stats()
        stats.game_active = True

        # Reinicia las imagenes de puntaje
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
