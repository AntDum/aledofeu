import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, length, width=0, height=0, color=(255,255,255), image=None, gravity=True, grav=(0,0.1)):
        """Init

        Args:\n
            x : pos x
            y : pos y
            angle : angle where the particle will go
            length : speed vector
            width (int, optional): width of the particle. Defaults to 0.
            height (int, optional): height of the particle. Defaults to 0.
            color (tuple, optional): color of the particle. Defaults to (255,255,255).
            image (pygame.Surface, optional): image of the particle. Defaults to None.
            gravity (bool, optional): is the particle has gravity. Defaults to True.
        """
        
        super().__init__()

        if image == None:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        else:
            self.image = image

        self.rect = self.image.get_rect()

        self.pos = pygame.math.Vector2(x, y)

        self.speed = pygame.math.Vector2(0,0)
        self.speed.from_polar((length, angle))

        self.acceleration = pygame.math.Vector2(0,0)

        if gravity:
            self.gravity = pygame.math.Vector2(grav[0], grav[1])
        else:
            self.gravity = pygame.math.Vector2(0, 0)

    def set_color(self, color):
       self.image.fill(color)

    def update(self, dt=1):
        self.speed += self.acceleration
        self.speed += self.gravity

        self.pos += self.speed * dt * 50

        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
    
    def draw(self, screen):
        screen.blit_cam(self.image, self.rect)


    def get_pos(self):
        return (self.pos.x, self.pos.y)


class ParticleSystem(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.has_finish = False

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)

    def remove_first(self, screen):
        if (len(self.sprites()) > 0):
            self.sprites()[0].kill()
