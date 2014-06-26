import pygame


class Bloc(pygame.sprite.Sprite):
    def __init__(self, width, height, x=0, y=0, *groups):
        super(Bloc, self).__init__(*groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color(255, 255, 0, 0))
        self.rect = pygame.Rect((x, y), (width, height))
#    def __init__(self, *groups):
#        super(Bloc, self).__init__(*groups)
#        self.image = pygame.Surface((1600, 600-436))
#        self.image.fill(pygame.Color(255, 255, 0, 0))
#        self.rect = pygame.Rect((0, 436), self.image.get_size())


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.sheet = pygame.image.load('Imatges/Spritesheet.png')
        self.animacio = []
        for x in range(0, 360, 72):
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

    def update(self, dt, game):
        if self.salta and self.tocant_terra(game):
            self.vy = -500
            self.salta = False
        if self.total_time < 0.01:
            self.total_time += dt
        else:
            self.total_time = 0
            self.current_image = (self.current_image + 1) % len(self.animacio)
        if (self.right and self.left) or (
                (not self.left) and (not self.right)):
            self.current_image = 0
            self.image = self.animacio[self.current_image]
        elif self.right:
            self.image = self.animacio[self.current_image]
            self.rect.x += self.vx * dt
        elif self.left:
            self.image = pygame.transform.flip(
                self.animacio[self.current_image], True, False)
            self.rect.x -= self.vx * dt

        top_terra = self.tocant_terra(game)
        if top_terra and top_terra > game.player.rect.top and self.vy >= 0:
            game.player.rect.bottom = top_terra + 1
            self.vy = 0
        else:
            self.rect.y += self.vy * dt + 0.5 * self.ay * dt * dt
            self.vy += self.ay * dt

    def tocant_terra(self, game):
        dict = pygame.sprite.groupcollide(
            game.playerG, game.blocs, False, False)
        if dict:
            max_top = max(map(lambda x: x.rect.top, dict[game.player]))
            if game.player.rect.bottom > max_top:
                return max_top
            else:
                return False


class Game (object):
    def main(self, screen):
        clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.blocs = pygame.sprite.Group()
        self.surt = False
        self.fons = pygame.image.load('Imatges/Fons.png')
        self.player = Player(self.sprites)
        self.playerG = pygame.sprite.GroupSingle(self.player)
#        self.terra = Bloc(self.blocs)
        self.terra = Bloc(1600, 600-436, 0, 436, self.blocs)
        Bloc(80, 20, 200, 300, self.blocs)
        Bloc(80, 20, 300, 200, self.blocs)

        while not self.surt:
            dt = clock.tick(30)
            self.gestiona_esdeveniments()
            self.update(dt/1000)
            self.draw(screen)

    def gestiona_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.surt = True
            elif event.type == pygame.KEYDOWN:
                self.gestiona_pressió(event)
            elif event.type == pygame.KEYUP:
                self.gestiona_alliberament(event)

    def gestiona_pressió(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.right = True
        elif event.key == pygame.K_LEFT:
            self.player.left = True
        elif event.key == pygame.K_UP:
            self.player.salta = True

    def gestiona_alliberament(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.right = False
        elif event.key == pygame.K_LEFT:
            self.player.left = False
        elif event.key == pygame.K_UP:
            self.player.salta = False

    def update(self, dt):
        self.sprites.update(dt, self)

    def draw(self, screen):
        screen.blit(self.fons, (0, 0))
        self.blocs.draw(screen)
        self.sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    Game().main(screen)
