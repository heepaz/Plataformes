import pygame


class Bloc(pygame.sprite.Sprite):
    def __init__(self, width, height, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color(255, 255, 0, 0))
        self.rect = pygame.Rect((x, y), (width, height))


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('Imatges/Spritesheet.png')
        # Creem una llista d'imatges a partir de trossets del "sheet"
        # que anomenarem "animacio"
        self.animacio = []
        # Des de 0 fins a 360, cada 72 píxels (l'amplada de cada imatge)
        for x in range(0, 360, 72):
            # Ho afegim com una imatge sola en la llista "animacio"
            self.animacio.append(
                self.sheet.subsurface(pygame.Rect(x, 0, 72, 72)))
        self.image = self.animacio[0]
        self.current_image = 0
        self.rect = pygame.Rect((20, 20), self.image.get_size())
        self.resting = False
        self.vx = 400
        self.vy = 0
        self.ay = 800
        self.right = False
        self.left = False
        self.salta = False
        self.total_time = 0

    def update(self, dt, joc):
        # Guardem la posició anterior per saber si les col·lisions són
        # de pujada o de baixada (només detectarem com a tal les segones)
        self.prev_pos = self.rect.copy()

        # Si el jugador vol saltar i està tocant el terra
        if self.salta and self.tocant_terra(joc):
            # Que salti!
            self.vy = -500
            self.salta = False

        # Ara ve el codi per l'animació i el moviment:
        # Si no ha passat prou temps per canviar d'imatge
        if self.total_time < 0.01:
            # Augmenta el temps que ha passat
            self.total_time += dt
        else:
            # Si ha passat prou temps, reinicia el comptador de temps
            self.total_time = 0
            # I fes que ensenyi la següent imatge de la animació.
            # Si s'ha acabat, torna a començar
            self.current_image = (self.current_image + 1) % len(self.animacio)

        # Si volem moure'ns cap a la dreta i l'esquerra alhora
        # o cap a cap dels dos llocs
        if (self.right and self.left) or (
                (not self.left) and (not self.right)):
            # No ens movem i utilitzem la primera imatge de l'animació
            # com a imatge per pintar
            self.current_image = 0
            self.image = self.animacio[self.current_image]
        # Si volem anar cap a la dreta
        elif self.right:
            # Agafem la imatge que toqui de l'animació com a imatge per pintar
            self.image = self.animacio[self.current_image]
            # I ens movem cap a la dreta
            self.rect.x += self.vx * dt
        # Si volem anar cap a l'esquerra
        elif self.left:
            # Afagem la imatge que toca de l'animació com a imatge per pintar
            # i la girem horitzontalment per tal que miri cap a l'esquerra
            self.image = pygame.transform.flip(
                self.animacio[self.current_image], True, False)
            # I ens movem cap a l'esquerra
            self.rect.x -= self.vx * dt

        # Ens movem avall
        self.rect.y += self.vy * dt + 0.5 * self.ay * dt * dt
        # Augmentem la velocitat vertical per causa de la gravetat
        self.vy += self.ay * dt
        top_terra = self.tocant_terra(joc)
        # Si estem tocant el terra i no ens estem movent cap amunt
        if top_terra and top_terra > joc.jugador.rect.top and self.vy >= 0:
            # Ens posem sobre el terra
            joc.jugador.rect.bottom = top_terra
            # I no caiem més
            self.vy = 0

    def tocant_terra(self, joc):
        # Fem una còpia de la posició del personatge per restaurar-la
        prev_rect = self.rect.copy()
        # Baixem el personatge un píxel perquè toqui el terra
        # Sinó, no detecta la col·lisió
        self.rect.y += 1
        # Mirem si el jugador col·lisiona amb algun sprite del grup blocs
        dict = pygame.sprite.groupcollide(
            joc.jugadorG, joc.blocs, False, False)
        if dict:
            # Agafem el punt més alt de tots els blocs amb què col·lisiona
            max_top = max(map(lambda x: x.rect.top, dict[joc.jugador]))
            # Mirem que la col·lisió sigui de baixada
            if self.rect.bottom >= max_top and (
                    self.prev_pos.bottom <= max_top):
                # Restaurem el personatge a la seva posició corresponent
                self.rect = prev_rect.copy()
                # Tornem el punt més alt
                return max_top
            else:
                # Si la col·lisió és de pujada...
                # Restaurem el personatge a la seva posició corresponent
                self.rect = prev_rect.copy()
                # Diem que no col·lisiona
                return False
        else:
            # Restaurem el personatge a la seva posició corresponent
            self.rect = prev_rect.copy()
            # Diem que no col·lisiona
            return False


class Game (object):
    def main(self, pantalla):
        self.alçada = pantalla.get_width()
        self.amplada = pantalla.get_height()

        clock = pygame.time.Clock()

        self.surt = False

        # Creem dos grups d'sprites
        self.sprites = pygame.sprite.Group()
        self.blocs = pygame.sprite.Group()

        self.fons = pygame.image.load('Imatges/Fons.png')

        # Creem un nou jugador i l'afegim al grup d'sprites "sprites"
        self.jugador = Jugador()
        self.jugador.add(self.sprites)
        # També creem un grup nou amb només l'sprite del jugador
        self.jugadorG = pygame.sprite.GroupSingle(self.jugador)

        # Creem un bloc, l'anomenem "terra" i l'afegim al grup
        # d'sprites "blocs" en dos passos
        self.terra = Bloc(2600, 600-436, -1000, 436)
        self.terra.add(self.blocs)
        # En creem i afegim dos més amb un sol pas cadascun
        Bloc(80, 20, 200, 300).add(self.blocs)
        Bloc(80, 20, 300, 200).add(self.blocs)

        while not self.surt:
            dt = clock.tick(30)
            self.gestiona_esdeveniments()
            self.update(dt/1000)
            self.draw(pantalla)

    def gestiona_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.surt = True
            elif event.type == pygame.KEYDOWN:
                self.gestiona_pressió(event)
            elif event.type == pygame.KEYUP:
                self.gestiona_alliberament(event)

    def gestiona_pressió(self, event):
        if event.key == pygame.K_ESCAPE:
            self.surt = True
        elif event.key == pygame.K_RIGHT:
            self.jugador.right = True
        elif event.key == pygame.K_LEFT:
            self.jugador.left = True
        elif event.key == pygame.K_UP:
            self.jugador.salta = True

    def gestiona_alliberament(self, event):
        if event.key == pygame.K_RIGHT:
            self.jugador.right = False
        elif event.key == pygame.K_LEFT:
            self.jugador.left = False
        elif event.key == pygame.K_UP:
            self.jugador.salta = False

    def update(self, dt):
        self.sprites.update(dt, self)

    def draw(self, pantalla):
        pantalla.blit(self.fons, (0, 0))
        self.blocs.draw(pantalla)
        self.sprites.draw(pantalla)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    amplada = 800
    alçada = 600
    pantalla = pygame.display.set_mode((amplada, alçada))
    Game().main(pantalla)
    pygame.quit()
