import pygame

import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Inicializa el juego y crea un objeto Settings y screen.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    # Crea un botton que diga "Play"
    play_button = Button(ai_settings, screen, "Play")
    # Crea un objeto GameStats
    stats = GameStats(ai_settings)
    # Crea un objeto Scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    # Crea una nave, un grupo para almacenar municiones y un grupo para almacenar aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Crea una flota de aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Inicia el bucle principal para el juego.
    while True:
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )


run_game()
