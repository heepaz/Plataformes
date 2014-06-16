import pygame


class Quadrat (object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def sobre(self):
        return self.y

    def sota(self):
        return self.y + self.h

    def esquerra(self):
        return self.x

    def dreta(self):
        return self.x + self.w

terra = Quadrat(0, 436, 1600, 600-436)


class Jugador (object):
    def __init__(self, x, y):
        self.imatge = pygame.image.load('Imatges/Personatge.png')
        self.w = self.imatge.get_width()
        self.h = self.imatge.get_height()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ay = 10

    def tocant_terra(self):
        return collisió(self.quadrat(), terra)

    def actualitza(self, dt):
        dt = dt/100
        self.x += self.vx * dt
        if self.tocant_terra() and self.vy >= 0:
            self.y = terra.sobre() - self.h
            self.vy = 0
        else:
            self.y += (self.vy * dt + 0.5 * self.ay * dt * dt)
            self.vy += self.ay * dt

    def dibuixa(self, pantalla):
        pantalla.blit(self.imatge, (self.x, self.y))

    def salta(self):
        self.vy = -50

    def quadrat(self):
        return Quadrat(self.x, self.y, self.w, self.h)


def collisió(quad1, quad2):
    if quad1.dreta() < quad2.esquerra():
        return False
    elif quad2.dreta() < quad1.esquerra():
        return False
    elif quad1.sota() < quad2.sobre():
        return False
    elif quad2.sota() < quad1.sobre():
        return False
    return True
