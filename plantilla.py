# -*- coding: utf-8 -*-

# Módulos
import pygame, sys
from pygame.locals import *
# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------

def main():
	''' Define la pantalla del programa '''
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	''' Define el nombre de la ventana'''
	pygame.display.set_caption("Not Pong")

	''' Carga de imagen para el fondo'''
	background_image = load_image('images/background1.jpg')

	''' Bucle de juego'''
	while True:
		''' Lista de eventos de pygame'''
		for eventos in pygame.event.get():
			#Si se hace click en la cruz de cierre, se cierra
			if eventos.type == QUIT:
				sys.exit(0)
		
		''' Funcion que carga la imagen de fondo '''
		screen.blit(background_image, (0, 0))
		''' Actualiza los cambios ocurridos en la pantalla'''
		pygame.display.flip()
	return 0
 
if __name__ == '__main__':
	pygame.init()
	main()