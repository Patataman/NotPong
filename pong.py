# -*- coding: utf-8 -*-

# Módulos
import pygame, sys, random
from pygame.locals import *
# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------
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
		self.speed = [mult1*0.35, mult2*0.35]

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

	def mover1(self, time, keys):
		if self.rect.top >= 0:
			# Flechita hacia arriba
			if keys[K_w]:
				self.rect.centery -= self.speed * time
		if self.rect.bottom <= HEIGHT:
			# Flechita hacia abajo
			if keys[K_s]:
				self.rect.centery += self.speed * time

	def mover2(self, time, keys):
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
	''' Define la pantalla del programa '''
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	''' Define el nombre de la ventana'''
	pygame.display.set_caption("Not Pong")

	''' Carga de imagen para el fondo'''
	background_image = load_image('images/fondo_pong.png')

	''' Carga de la pelotica '''
	bola = Bola()

	''' Carga jugador (a 30px de la izq)'''
	pala_jug = Pala(30)

	''' Carga cou (a 30px a la drch)'''
	pala_cpu = Pala(WIDTH - 30)
	pala_cpu.speed = 0.4

	''' Reloj de juego '''
	clock = pygame.time.Clock()

	''' Puntuacion de los jugadores [J1, J2]'''
	puntos = [0, 0]

	''' Bucle de juego'''
	while True:

		time = clock.tick(60)
		keys = pygame.key.get_pressed()
		''' Lista de eventos de pygame'''
		for eventos in pygame.event.get():
			#Si se hace click en la cruz de cierre, se cierra
			if eventos.type == QUIT:
				sys.exit(0)
		
		#Actualizar la posicion de la pelota y de la pala
		puntos = bola.actualizar(time, pala_jug, pala_cpu, puntos)
		pala_jug.mover1(time, keys)
		pala_cpu.mover2(time, keys)
		p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH/4, 40)
		p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH-WIDTH/4, 40)


		''' Actualiza los cambios ocurridos en la pantalla'''
		screen.blit(background_image, (0, 0))
		screen.blit(bola.image, bola.rect)
		screen.blit(pala_jug.image, pala_jug.rect)
		screen.blit(pala_cpu.image, pala_cpu.rect)
		screen.blit(p_jug, p_jug_rect)
		screen.blit(p_cpu, p_cpu_rect)
		pygame.display.flip()
	return 0
 
if __name__ == '__main__':
	pygame.init()
	main()
