import pygame
from pygame.sprite import Sprite


class Ship(Sprite):  # Clase que gestiona las configuraciones de la nave
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carga la imagen de la nava y obtiene su rectángulo.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Inicia cada nueva nave en la parte inferior central de la pantalla.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Guarda un valor decimal para el centro de la nave.
        self.center = float(self.rect.centerx)

        # Banderas de movimiento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Actualiza la posicion de la nave basado en la bandera de movimento.
        # Actualiza el valor central de la nave, no el rectangulo.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Actualiza el objeto rect desde el self.center.
        self.rect.centerx = self.center

    def blitme(self):
        # Dibuja la nave en su posición actual.
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Centra la nave en la pantalla.
        self.center = self.screen_rect.centerx
