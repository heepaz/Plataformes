#!/usr/bin/env python3
import pygame
from pygame.locals import *
from personatges import Jugador

# Iniciem el pygame
pygame.init()

# Definim les mides de la pantalla que volem crear
AMPLADA = 800
ALÇADA = 600
pantalla = pygame.display.set_mode((AMPLADA, ALÇADA), 0, 32)

# Posem títol a la finestra
pygame.display.set_caption('Plataformes')

# Carrega el fons
fons = pygame.image.load('Imatges/Fons.png')

# Creen un rellotge
rellotge = pygame.time.Clock()

# En principi no volem sortir del joc
surt = False


def inicia_joc():
    global personatges, rellotge, jugador
    rellotge.tick()
    personatges = []
    jugador = Jugador(30, 20)
    personatges.append(jugador)


def gestiona_pressió(event):
    if event.key == K_UP:
        if jugador.tocant_terra():
            jugador.salta()


def gestiona_alliberament(event):
    return


def gestiona_entrada():
    global surt
    for event in pygame.event.get():
        if event.type == QUIT:
            surt = True
        elif event.type == KEYDOWN:
            gestiona_pressió(event)
        elif event.type == KEYUP:
            gestiona_alliberament(event)


def actualitza(dt):
    for personatge in personatges:
        personatge.actualitza(dt)


def pinta():
    pantalla.blit(fons, (0, 0))
    for personatge in personatges:
        personatge.dibuixa(pantalla)
    pygame.display.update()


def loop_principal():
    while not surt:
        dt = rellotge.tick()
        gestiona_entrada()
        actualitza(dt)
        pinta()


if __name__ == '__main__':
    inicia_joc()
    loop_principal()
