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

    def pinta(self, pantalla):
        pygame.draw.rect(pantalla,
                         pygame.Color(0, 255, 0, 0),
                         pygame.Rect(self.x, self.y, self.w, self.h))


class Jugador (object):
    def __init__(self, x, y):
        self.imatge = pygame.image.load('Imatges/Spritesheet.png')
        self.w = self.imatge.get_width()
        self.h = self.imatge.get_height()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ay = 10
        self.e = False
        self.d = False
        self._VX = 30

    def tocant_terra(self, terra):
        return collisió(self.quadrat(), terra)

    def actualitza(self, dt):
        global terra
        dt = dt/100
        if self.d and self.e:
            self.vx = 0
        elif self.d:
            self.vx = self._VX
        elif self.e:
            self.vx = -self._VX
        else:
            self.vx = 0

        self.x += self.vx * dt

        if self.tocant_terra(terra) and self.vy >= 0:
            self.y = terra.sobre() - self.h
            self.vy = 0
        else:
            self.y += (self.vy * dt + 0.5 * self.ay * dt * dt)
            self.vy += self.ay * dt

    def dibuixa(self, pantalla):
        pantalla.blit(self.imatge, (self.x, self.y))

    def salta(self):
        if self.tocant_terra():
            self.vy = -60

    def dreta(self):
        self.d = True

    def esquerra(self):
        self.e = True

    def prou_dreta(self):
        self.d = False

    def prou_esquerra(self):
        self.e = False

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
