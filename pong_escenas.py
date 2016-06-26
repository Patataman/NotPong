# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random
from pygame.locals import *
# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------
class Director:
	"""Representa el objeto principal del juego.

	El objeto Director mantiene en funcionamiento el juego, se
	encarga de actualizar, dibuja y propagar eventos.

	Tiene que utilizar este objeto en conjunto con objetos
	derivados de Scene."""

	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("Not Pong")
		self.scene = None
		self.quit_flag = False
		self.clock = pygame.time.Clock()

	def loop(self):
		"Pone en funcionamiento el juego."

		while not self.quit_flag:
			time = self.clock.tick(60)

			# Eventos de Salida
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.quit()

			# detecta eventos
			self.scene.on_event()

			# actualiza la escena
			self.scene.on_update()

			# dibuja la pantalla
			self.scene.on_draw(self.screen)
			pygame.display.flip()

	def change_scene(self, scene):
		"Altera la escena actual."
		self.scene = scene

	def quit(self):
		self.quit_flag = True

class Scene:
    """Representa un escena abstracta del videojuego.
 
    Una escena es una parte visible del juego, como una pantalla
    de presentación o menú de opciones. Tiene que crear un objeto
    derivado de esta clase para crear una escena utilizable."""
 
    def __init__(self, director):
        self.director = director
 
    def on_update(self):
        "Actualización lógica que se llama automáticamente desde el director."
        raise NotImplemented("Tiene que implementar el método on_update.")
 
    def on_event(self, event):
        "Se llama cuando llega un evento especifico al bucle."
        raise NotImplemented("Tiene que implementar el método on_event.")
 
    def on_draw(self, screen):
        "Se llama cuando se quiere dibujar la pantalla."
        raise NotImplemented("Tiene que implementar el método on_draw.")

class SceneHome(Scene):
    """Escena inicial del juego, esta es la primera que se carga cuando inicia"""
    
    iniciar = None
    iniciar_rect = None
    options = None
    options_rect = None
    titulo = None
    titulo_rect = None

    def __init__(self, director):
        Scene.__init__(self, director)
    	#Altura: Segundo cuarto
    	self.iniciar, self.iniciar_rect = texto('Iniciar', WIDTH/2, HEIGHT/2)
    	#Altura: Tercer cuatro
    	self.options, self.options_rect = texto('Opciones', WIDTH/2, 3*HEIGHT/4)
    	self.titulo, self.titulo_rect = texto('Not Pong', WIDTH/2, HEIGHT/4, (255,255,255), 75)

    	#Carga la musica
    	pygame.mixer.music.load("music/title_theme.mp3")
    	#Pone la música a funcionar
    	# loop = -1 -> Loop infinito
    	pygame.mixer.music.play(-1)
        
    def on_update(self):
        pass
 
    def on_event(self):
		keys = pygame.key.get_pressed()
		#Flechita hacia arriba
		if keys[K_UP]:
			#Altura: Segundo cuarto
			self.iniciar, self.iniciar_rect = texto('Iniciar', WIDTH/2, HEIGHT/2, (250,255,78))
			#Altura: Tercer cuatro
			self.options, self.options_rect = texto('Opciones', WIDTH/2, 3*HEIGHT/4, (255,255,255))
		# Flechita hacia abajo
		if keys[K_DOWN]:
			self.iniciar, self.iniciar_rect = texto('Iniciar', WIDTH/2, HEIGHT/2, (255,255,255))
			#Altura: Tercer cuatro
			self.options, self.options_rect = texto('Opciones', WIDTH/2, 3*HEIGHT/4, (250,255,78))
 
    def on_draw(self, screen):
    	#Renderiza las letras
    	screen.blit(self.titulo, self.titulo_rect)
    	screen.blit(self.iniciar, self.iniciar_rect)
    	screen.blit(self.options, self.options_rect)

class SceneGame(Scene):
	"""Escena del bucle de juego"""

	def __init__(self, director):
		Scene.__init__(self, director)
		pygame.mixer.music.stop()

	def on_update(self):
		pass

	def on_event(self):
		pass

	def on_draw(self, screen):
		pass

class SceneOptions(Scene):
	"""Escena del bucle de juego"""

	def __init__(self, director):
		Scene.__init__(self, director)

	def on_update(self):
		pass

	def on_event(self):
		pass

	def on_draw(self, screen):
		pass

''' Clase para el sprite de la pelota'''
class Bola(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("images/ball.png", True)

		''' 
			self.image.get_rect() tiene las siguientes propiedades:
			- top, left, bottom, right
			- topleft, bottomleft, topright, bottomright
			- midtop, midleft, midbottom, midright
			- center, centerx (posición central del sprite en el eje horizontal), centery
			- size, width, height
			- w, h
		'''
		self.rect = self.image.get_rect()

		#Se coloca la peloca en el centro de la ventana
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2

		#Velocidad en el eje X, eje Y
		self.speed = [0.5, -0.5]

	def reset(self):
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2
		if random.random() > 0.45: 
			mult1 = -1
			mult2 = 1
		else:
			mult1 = 1
			mult2 = -1
		self.speed = [mult1*random.uniform(0.3, 0.6), mult2*random.uniform(0.3, 0.6)]

	def actualizar(self, time, pala_jug, pala_cpu, puntos):
		# Espacio = V * T
		self.rect.centerx += self.speed[0] * time
		self.rect.centery += self.speed[1] * time

		if self.rect.left <= 0:
			puntos[1] += 1
			self.reset()
		if self.rect.right >= WIDTH-15:
			puntos[0] += 1
			self.reset()

		if self.rect.left <= 0 or self.rect.right >= WIDTH:
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time
		if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
			self.speed[1] = -self.speed[1]
			self.rect.centery += self.speed[1] * time
		#Si colisiona la pelota y la pala del jugador...
		if pygame.sprite.collide_rect(self, pala_jug):
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time

		#Si colisiona la pelota y la pala de la cpu...
		if pygame.sprite.collide_rect(self, pala_cpu):
			self.speed[0] = -self.speed[0]
			self.rect.centerx += self.speed[0] * time

		return puntos


class Pala(pygame.sprite.Sprite):
	def __init__(self, x):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("images/pala.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = HEIGHT / 2
		self.speed = 0.5

	def mover(self, time, keys):
		if self.rect.top >= 0:
			# Flechita hacia arriba
			if keys[K_UP]:
				self.rect.centery -= self.speed * time
		if self.rect.bottom <= HEIGHT:
			# Flechita hacia abajo
			if keys[K_DOWN]:
				self.rect.centery += self.speed * time

	def ia(self, time, ball):
		if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
			if self.rect.centery < ball.rect.centery:
				self.rect.centery += self.speed * time
			if self.rect.centery > ball.rect.centery:
				self.rect.centery -= self.speed * time



# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
	''' Intenta abrir la imagen dada por la ruta "filename" '''
	try: image = pygame.image.load(filename)
	#Si falla, sale el error
	except pygame.error, message:
		raise SystemExit, message
	''' Convierte la imagen a una de tipo de pygame'''
	image = image.convert()
	''' Si la imagen tiene transparencia, toma como transparencia el pixel superior izquierdo'''
	if transparent:
		color = image.get_at((0,0))
		image.set_colorkey(color, RLEACCEL)
	return image

''' Escribir texto '''

def texto(texto, posx, posy, color=(255, 255, 255), size=25):
    fuente = pygame.font.Font("fonts/DroidSans.ttf", size)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# ---------------------------------------------------------------------

def main():
	dir = Director()
	scene = SceneHome(dir)
	dir.change_scene(scene)
	dir.loop()
 
if __name__ == '__main__':
	pygame.init()
	main()
