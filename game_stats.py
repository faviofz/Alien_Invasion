class GameStats:
    # Seguimiento de estadisticas para Alien Invasion.
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # Inicia Alien Invasion en un estado inactivo.
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        # Inicializa estadísticas que pueden cambiar durante el juego.
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
