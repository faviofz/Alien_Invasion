import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):  # Clase que gestiona las municiones de la nave
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Crea un rectángulo de la munición en (0,0) y establece la posición correcta.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Almacena la posicion de la munición como un valor decimal.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Acualiza la posicion decimal de la munición.
        self.y -= self.speed_factor
        # Actualiza la posición del rectángulo.
        self.rect.y = self.y

    def draw_bullet(self):
        # Dibuja la munición en la pantalla.
        pygame.draw.rect(self.screen, self.color, self.rect)
