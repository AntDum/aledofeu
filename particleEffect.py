import pygame
import particleSystem
from random import randint, uniform


class FireWork(particleSystem.ParticleSystem):
    def __init__(self, x, y, timer=1, amount=20, life_time=4, missile_size=5, particule_size=2,color=None, missile_color=(200, 215, 200), FPS=60):
        super().__init__()

        self.pos = pygame.math.Vector2(x, y)
        self.timer = timer*FPS
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.color = color
        self.size = particule_size
        self.has_exploded = False
        self.has_finish = False
        p = particleSystem.Particle(
            self.pos[0], self.pos[1], 
            -90, 15, missile_size, missile_size, 
            color=missile_color, gravity=False)
        self.add(p)

    def explode(self, screen):
        self.pos.x = self.sprites()[0].get_pos()[0]
        self.pos.y = self.sprites()[0].get_pos()[1]
        self.empty()
        for _ in range(self.amount):
            size = randint(-2,2) + self.size
            if self.color == None:
                if randint(0,1) > 0:
                    color = (randint(0, 15),randint(230, 255),randint(0, 15))
                else:
                    color = (randint(230, 255),randint(200, 230),randint(0, 15))
            else:
                color = self.color
            p = particleSystem.Particle(self.pos[0], self.pos[1], randint(0, 360),
                    randint(1, 4), size, size, color=color, gravity=True)
            self.add(p)

    def draw(self, screen):
        self.count += 1
        if not self.has_exploded and self.timer <= self.count:
            self.explode(screen)
            self.count = 0
            self.has_exploded = True

        if self.has_exploded and self.life_time <= self.count:
            self.empty()
            self.has_finish = True

        super().draw(screen)


class Dust(particleSystem.ParticleSystem):
    def __init__(self, x, y, life_time=1, color=None, gravity=True, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = int(life_time)*FPS
        self.count = 0
        self.color = color
        self.gravity = gravity

    def draw(self, screen):
        self.count += 1

        size = randint(3, 10)

        if self.color == None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        else:
            color = self.color

        self.add(particleSystem.Particle(self.pos[0], self.pos[1], randint(
            0, 360), randint(1, 2), size, size, color=color, gravity=self.gravity))

        if self.count >= self.life_time:
            self.remove_first(screen)

        super().draw(screen)

        

class Explosion(particleSystem.ParticleSystem):
    def __init__(self, x, y, amount=20, life_time=1, color=None, size=None, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.amount_count = amount
        self.color = color
        self.size = size

    def explode(self):
        self.amount_count += self.amount
        self.has_finish = False
        for _ in range(self.amount):
            if (self.size == None):
                size = randint(5, 10)
            else:
                size = self.size
            if self.color == None:
                color = (randint(0, 255), randint(0, 255), randint(0, 255))
            else:
                color = self.color
                
            self.add(particleSystem.Particle(self.pos[0], self.pos[1], 
                            randint(0, 360), uniform(3,6), 
                            size, size, color=color, 
                            gravity=False))
        return self

    def draw(self, screen):
        self.count += 1

        if self.life_time <= self.count:
            for _ in range(randint(self.amount//20,self.amount//5)):
                self.remove_first(screen)
                self.amount_count -= 1
        
        if self.amount_count <= 0:
            self.has_finish = True

        super().draw(screen)



class FireExplosion(particleSystem.ParticleSystem):
    def __init__(self, x, y, amount=20, life_time=1, color=None, size=None, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.amount_count = amount
        self.color = color
        self.size = size

    def explode(self):
        self.amount_count += self.amount
        self.has_finish = False
        for _ in range(self.amount):
            if (self.size == None):
                size = randint(5, 10)
            else:
                size = self.size + randint(-1,1)
            if self.color == None:
                ran = randint(0,3)
                if ran > 1:
                    color = (randint(200, 255), randint(0, 15), randint(0, 15))
                elif ran > 0:
                    color = (randint(240, 255),randint(100, 150),0)
                else:
                    ore = randint(220, 240)
                    color = (randint(240, 255), ore, ore)
            else:
                color = self.color
                
            self.add(particleSystem.Particle(self.pos[0], self.pos[1], 
                            randint(0,360), uniform(1,3), 
                            size, size, color=color, 
                            gravity=True, grav=(0,-0.1)))
        return self

    def draw(self, screen):
        self.count += 1

        if self.life_time <= self.count:
            for _ in range(randint(self.amount//20,self.amount//5)):
                self.remove_first(screen)
                self.amount_count -= 1
        
        if self.amount_count <= 0:
            self.has_finish = True

        super().draw(screen)


class Smoke(particleSystem.ParticleSystem):
    def __init__(self, x, y, amount=20, life_time=1, color=None, size=None, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.amount_count = amount
        self.color = color
        self.size = size

    def explode(self):
        self.amount_count += self.amount
        self.has_finish = False
        for _ in range(self.amount):
            if (self.size == None):
                size = randint(5, 10)
            else:
                size = self.size + randint(-1,1)
            if self.color == None:
                ore = randint(50,200)
                color = (ore, ore, ore)
            else:
                color = self.color
                
            self.add(particleSystem.Particle(self.pos[0], self.pos[1], 
                            randint(-20, 20)-90, uniform(1,4), 
                            size, size, color=color, 
                            gravity=True, grav=(0,-0.05)))
        return self

    def draw(self, screen):
        self.count += 1

        if self.life_time <= self.count:
            for _ in range(randint(self.amount//20,self.amount//5)):
                self.remove_first(screen)
                self.amount_count -= 1
        
        if self.amount_count <= 0:
            self.has_finish = True

        super().draw(screen)


class LandExplosion(particleSystem.ParticleSystem):
    def __init__(self, x, y, amount=20, life_time=1, color=None, size=None, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.amount_count = amount
        self.color = color
        self.size = size

    def explode(self):
        self.amount_count += self.amount
        self.has_finish = False
        for _ in range(self.amount):
            if (self.size == None):
                size = randint(5, 10)
            else:
                size = self.size
            if self.color == None:
                ore = randint(50,120)
                color = (ore, ore, ore)
            else:
                color = self.color
                
            self.add(particleSystem.Particle(self.pos[0], self.pos[1], 
                            randint(-90, 90) -90, uniform(0.5,2), 
                            size, size, color=color, 
                            gravity=False))
        return self

    def draw(self, screen):
        self.count += 1

        if self.life_time <= self.count:
            for _ in range(randint(self.amount//20,self.amount//5)):
                self.remove_first(screen)
                self.amount_count -= 1
        
        if self.amount_count <= 0:
            self.has_finish = True

        super().draw(screen)
        

class RewardExplosion(particleSystem.ParticleSystem):
    def __init__(self, x, y, amount=20, life_time=1, color=None, size=None, FPS=60):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.life_time = life_time*FPS
        self.count = 0
        self.amount = amount
        self.amount_count = amount
        self.color = color
        self.size = size

    def explode(self):
        self.amount_count += self.amount
        self.has_finish = False
        for _ in range(self.amount):
            size = randint(-2,2) + self.size
            if self.color == None:
                if randint(0,1) > 0:
                    color = (randint(0, 15),randint(230, 255),randint(0, 15))
                else:
                    color = (randint(230, 255),randint(200, 230),randint(0, 15))
            else:
                color = self.color
                
            self.add(particleSystem.Particle(self.pos[0], self.pos[1], randint(0, 360),
                    randint(1, 4), size, size, color=color, gravity=True))
        return self

    def draw(self, screen):
        self.count += 1

        if self.life_time <= self.count:
            for _ in range(randint(self.amount//20,self.amount//5)):
                self.remove_first(screen)
                self.amount_count -= 1
        
        if self.amount_count <= 0:
            self.has_finish = True

        super().draw(screen)