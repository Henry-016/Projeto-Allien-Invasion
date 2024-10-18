class GameStats:
    """Aramazena Dados Estatísticos da Invasão Alien"""

    def __init__(self, ai_settings):
        """Inicializa os Dados Estatísticos"""

        self.ai_settings = ai_settings
        self.reset_stats()
        self.high_score = self.load_high_score()
        self.game_active = False

    def reset_stats(self):
        """Inicializa os Dados Estatísticos que Podem Mudar Durante o Jogo"""

        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Salva o high score em um arquivo"""
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        """Carrega o high score de um arquivo, se existir. Caso contrário, cria o arquivo."""
        try:
            with open('high_score.txt', 'r') as file:
                high_score = int(file.read())
        except FileNotFoundError:
            # Se o arquivo não existir, cria o arquivo com 0 como pontuação inicial
            with open('high_score.txt', 'w') as file:
                file.write('0')
            high_score = 0  # Define o high score como 0
        except ValueError:
            # Caso o conteúdo do arquivo seja inválido, também retorna 0
            high_score = 0

        return high_score
