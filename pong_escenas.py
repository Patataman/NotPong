# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random
from pygame.locals import *
# Constantes
MUSIC = 1
RES = 0%3
RESOLUTION = [(640,480), (800,600), (1024,768)]
WIDTH = RESOLUTION[RES][0]
HEIGHT = RESOLUTION[RES][1]

# Clases
# ---------------------------------------------------------------------
class Director:
	"""Representa el objeto principal del juego.

	El objeto Director mantiene en funcionamiento el juego, se
	encarga de actualizar, dibuja y propagar eventos.

	Tiene que utilizar este objeto en conjunto con objetos
	derivados de Scene."""

	def __init__(self):
		self.screen = pygame.display.set_mode(RESOLUTION[0])
		pygame.display.set_caption("Not Pong")
		self.scene = None
		self.quit_flag = False
		self.clock = pygame.time.Clock()

	def loop(self):
		"Pone en funcionamiento el juego."

		pygame.key.set_repeat(10, 200)
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
				self.scene.on_event(time, event)
			# actualiza la escena
			self.scene.on_update(time)

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

	def __init__(self, director):
		Scene.__init__(self, director)

		#Altura: Segundo cuarto
		self.iniciar, self.iniciar_rect = texto('Iniciar', WIDTH/2, HEIGHT/2+20)
		#Altura: Tercer cuatro
		self.options, self.options_rect = texto('Opciones', WIDTH/2, 3*HEIGHT/4)
		self.titulo, self.titulo_rect = texto('Not Pong', WIDTH/2, HEIGHT/4, (255,255,255), 75)

		self.menu = [self.iniciar, self.options]
		self.alturas = [HEIGHT/2+20, 3*HEIGHT/4]

		self.selected = 0

		self.flecha = load_image("images/flecha.png")
		self.flecha = pygame.transform.scale(self.flecha, (self.iniciar.get_width()/2+10,self.iniciar.get_height()/2+10))
		self.flecha_rect = self.flecha.get_rect()
		self.flecha_rect.centerx = WIDTH/2 - self.menu[self.selected].get_width()
		self.flecha_rect.centery = self.alturas[self.selected]

		#Carga la musica
		if not pygame.mixer.music.get_busy() and MUSIC == 1:
			pygame.mixer.music.load("music/title_theme.mp3")
			#Pone la música a funcionar
			# loop = -1 -> Loop infinito
			pygame.mixer.music.play(-1)

	def on_update(self, time):
		pass

	def on_event(self, time, event):
		#Flechita hacia arriba
		keys = pygame.key.get_pressed()
		if pygame.KEYDOWN:
			if keys[K_UP]:
				self.selected = self.selected - 1 if self.selected > 0 else 0
				self.flecha_rect.centery = self.alturas[self.selected]
			# Flechita hacia abajo
			if keys[K_DOWN]:
				self.selected = self.selected + 1 if self.selected<(len(self.menu)-1) else self.selected
				self.flecha_rect.centery = self.alturas[self.selected]
	 		
			if keys[K_RETURN]:
				if self.selected == 0:
					scene = SceneGame(self.director)
					self.director.change_scene(scene)
				if self.selected == 1:
					scene = SceneOptions(self.director)
					self.director.change_scene(scene)			

	def on_draw(self, screen):
		#Renderiza las letras
		screen.fill((0,0,0))
		screen.blit(self.titulo, self.titulo_rect)
		screen.blit(self.flecha, self.flecha_rect)
		screen.blit(self.iniciar, self.iniciar_rect)
		screen.blit(self.options, self.options_rect)

class SceneOptions(Scene):
	"""Escena del bucle de juego"""

	def __init__(self, director):
		Scene.__init__(self, director)
		#Altura: Segundo cuarto
		self.musica, self.musica_rect = texto('Musica', WIDTH/2, HEIGHT/2+20)
		#Altura: Tercer cuatro
		self.resol, self.resol_rect = texto('Resolucion (No furula)', WIDTH/2, 3*HEIGHT/4)
		self.atras, self.atras_rect = texto('Atras', WIDTH/6, HEIGHT-40)
		self.titulo, self.titulo_rect = texto('Not Pong', WIDTH/2, HEIGHT/4, (255,255,255), 75)

		self.menu = [self.musica, self.resol, self.atras]
		self.dim = [[WIDTH/2, HEIGHT/2+20], [WIDTH/2,3*HEIGHT/4], [WIDTH/6,HEIGHT-40]]

		self.selected = 0

		self.flecha = load_image("images/flecha.png")
		self.flecha = pygame.transform.scale(self.flecha, (self.musica.get_width()/2+10,self.musica.get_height()/2+10))
		self.flecha_rect = self.flecha.get_rect()
		self.flecha_rect.centerx = self.dim[self.selected][0] - self.menu[self.selected].get_width()/2 - 20
		self.flecha_rect.centery = self.dim[self.selected][1]

	def on_update(self, time):
		pass

	def on_event(self, time, event):
		keys = pygame.key.get_pressed()

		if pygame.KEYDOWN:
			#Flechita hacia arriba
			if keys[K_UP]:
				self.selected = self.selected - 1 if self.selected > 0 else 0
				self.flecha_rect.centery = self.dim[self.selected][1]
				self.flecha_rect.centerx = self.dim[self.selected][0] - self.menu[self.selected].get_width()/2 - 20
			# Flechita hacia abajo
			if keys[K_DOWN]:
				self.selected = self.selected + 1 if self.selected<(len(self.menu)-1) else self.selected
				self.flecha_rect.centery = self.dim[self.selected][1]
				self.flecha_rect.centerx = self.dim[self.selected][0] - self.menu[self.selected].get_width()/2 - 20
	 		
			if keys[K_RETURN]:
				if self.selected == 0:
					global MUSIC
					MUSIC = 0 if MUSIC == 1 else 1
					if MUSIC == 0:
						pygame.mixer.music.stop()
					if MUSIC == 1:
						pygame.mixer.music.load("music/title_theme.mp3")
						pygame.mixer.music.play(-1)
				if self.selected == 2:
					scene = SceneHome(self.director)
					self.director.change_scene(scene)

	def on_draw(self, screen):
		#Renderiza las letras
		screen.fill((0,0,0))
		screen.blit(self.titulo, self.titulo_rect)
		screen.blit(self.flecha, self.flecha_rect)
		screen.blit(self.musica, self.musica_rect)
		screen.blit(self.resol, self.resol_rect)
		screen.blit(self.atras, self.atras_rect)

class SceneGame(Scene):
	"""Escena del bucle de juego"""

	def __init__(self, director):
		Scene.__init__(self, director)
		pygame.key.set_repeat(10, 10)
		pygame.mixer.music.stop()
		if MUSIC == 1:
			pygame.mixer.music.load("music/game_theme.mp3")
			pygame.mixer.music.play(-1)

		''' Define el nombre de la ventana'''
		#pygame.display.set_caption("Not Pong")

		''' Carga de imagen para el fondo'''
		self.background_image = load_image('images/fondo_pong.png')

		''' Carga de la pelotica '''
		self.bola = Bola()

		''' Carga jugador (a 30px de la izq)'''
		self.pala_jug = Pala(30)

		''' Carga cou (a 30px a la drch)'''
		self.pala_cpu = Pala(WIDTH - 30)
		self.pala_cpu.speed = 0.4

		''' Reloj de juego '''
		#self.clock = pygame.time.Clock()

		''' Puntuacion de los jugadores [J1, J2]'''
		self.puntos = [0, 0]


	def on_update(self, time):
		#Actualizar la posicion de la pelota y de la pala
		self.puntos = self.bola.actualizar(time, self.pala_jug, self.pala_cpu, self.puntos)
		self.pala_cpu.ia(time, self.bola)
		self.p_jug, self.p_jug_rect = texto(str(self.puntos[0]), WIDTH/4, 40)
		self.p_cpu, self.p_cpu_rect = texto(str(self.puntos[1]), WIDTH-WIDTH/4, 40)

	def on_event(self, time, event):
		keys = pygame.key.get_pressed()
		
		self.pala_jug.mover(time, keys)

	def on_draw(self, screen):
		''' Actualiza los cambios ocurridos en la pantalla '''
		screen.blit(self.background_image, (0, 0))
		screen.blit(self.bola.image, self.bola.rect)
		screen.blit(self.pala_jug.image, self.pala_jug.rect)
		screen.blit(self.pala_cpu.image, self.pala_cpu.rect)
		screen.blit(self.p_jug, self.p_jug_rect)
		screen.blit(self.p_cpu, self.p_cpu_rect)

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
