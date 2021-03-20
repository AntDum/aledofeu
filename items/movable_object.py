import pygame as pg

class MovableObject(pg.sprite.Sprite):
    
    def __init__(self, x=0, y=0, image=None, tile_size=32, is_hard=True, is_liftable=False, gravity=0.75, has_gravity=False, map=None):
        super().__init__()
        
        self.tile_size = tile_size
        self.liftable = False
        if image == None:
            self.image = pg.Surface((tile_size,tile_size))
            self.image.fill((48,212,32))
        else:
            self.image = image
        
        self.gravity = gravity
        self.vel = pg.math.Vector2(0,0)
        self.has_gravity = has_gravity
        
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect
        
        self.pos = pg.Vector2(x*tile_size, y*tile_size)
        
        self.is_hard = is_hard
        self.is_liftable = is_liftable
        
        # self.speedfact_x = 50
        # self.speedfact_y = 50
        
        self.map = map
        
        self.iteration = 0
        
        self.update_end()
    
    def update(self, dt):
        self.update_init(dt)
        self.update_middle(dt)
        self.update_end(dt)
    
    def update_init(self, dt=1):
        self.prev_rect = pg.Rect(self.rect)
    
    def update_middle(self, dt=1):
        if self.has_gravity:
            self.vel.y += self.gravity
            self.pos += self.vel * dt * 50
            if (self.map.collide_with_tile(self, 'y')) == "S":
                self.has_gravity = False
                
    def update_end(self, dt=1):
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        self.iteration += 1
    
    def draw(self, screen):
        screen.blit_cam(self.image, self.rect)

    def set_pos(self, x, y):
        self.pos.x = x * self.tile_size
        self.pos.y = y * self.tile_size


class Liftable(MovableObject):
    """
    Class for buckets and furnitures that can be lifted by the players
    """
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None):
        super().__init__(x, y, image, tile_size, is_hard=False, is_liftable=True, map=map)
        self.image.fill((212,48,32))
        self.speedfact_x = 30
        self.speedfact_y = 40
        
class Container(MovableObject):
    """
    Class for all furnitures that can be looted by the player
    """
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None):
        super().__init__(x, y, image, tile_size, is_hard=False, map=map)
        self.image.fill((48,32,212))