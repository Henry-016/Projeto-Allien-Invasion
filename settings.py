class Settings:
	"""Uma Classe pra Armazenar todas as Configurações do Jogo Invasão Alienigena"""
	
	def __init__(self):
		"""Incializa as Configurações do Jogo"""
		
		# Configurações da Tela
		
		self.screen_width = 900
		self.screen_height = 514
		self.bg_color = (230, 230, 230)
		
		# Configurações da Nave
		
		self.ship_limit = 3
		
		# Configurações dos Projéteis
		
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		
		# Configurações dos Aliens
		
		self.fleet_drop_speed = 10
		
		# A Taxa pela qual a Velocidade do Jogo Aumenta

		self.speedup_scale = 1.1
		
		self.initialize_dynamic_settings()
		
		# A Taxa pela qual os Pontos para cada Aliens Aumenta de Acordo com a Dificuldade
		
		self.score_scale = 1.5
		
	def initialize_dynamic_settings(self):
		"""Inicializa as Configurações que Mudam ao Decorrer do Jogo"""
		
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		# Pontuação
		
		self.alien_points = 50
		
		# fleet_direction Igual a 1 Representa a Direita / -1 Representa a Esquerda
		
		self.fleet_direction = 1

	def increase_speed(self):
		"""Aumenta as Configurações de Velocidade"""
		
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		# Aumento da Pontuação
		
		self.alien_points = int(self.alien_points * self.score_scale)
