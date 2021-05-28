class Settings:  # Una clase para almacenar todas las configuraciones del juego.
    def __init__(self):  # Inicializa las configuraciones del juego.
        # Configuraciones de pantalla.
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Configuraciones de la nave.
        self.ship_limit = 3

        # Configuraciones de las municiones.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Configuraciones del alien.
        self.fleet_drop_speed = 10

        # Que tan rapido avanza el juego
        self.speedup_scale = 1.1

        # Que tan rapido incrementa el valor de un alien.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5  # Moveremos la nave 1.5 pixeles en lugar de 1 pixel.
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction en 1 representa derecha; -1 representa izquierda.
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
