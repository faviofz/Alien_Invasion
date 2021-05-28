import pygame

from pygame.sprite import Sprite


class Alien(Sprite):  # Una clase para representar un alien.
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carga el alien y establece sus atributos rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Inicia cada alien cerca de la parte superior izquierda de la pantalla.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posicion exacta del alien
        self.x = float(self.rect.x)

    def blitme(self):
        # Dibuja el alien en su posicion actual.
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Mueve el alien a izquierda o derecha.
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        # Retorna True si el alien está al filo de la pantalla.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
