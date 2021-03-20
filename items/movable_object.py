import pygame as pg
import os

TILES_SIZE = 32

def get_image(name, scale):
    return pg.transform.scale(pg.image.load(os.path.join("res","Tile",f"{name}.png")), scale)

def get_image_fire(name, scale):
    return pg.transform.scale(pg.image.load(os.path.join("res","fire",f"{name}.png")), scale)

wall_sprite = get_image("Wall", (TILES_SIZE,TILES_SIZE))
woodBackGround_sprite = get_image("Wood_backGround", (TILES_SIZE,TILES_SIZE))
bed_sprite = get_image("bed_picture", (TILES_SIZE,TILES_SIZE))
chairLeft_sprite = get_image("chair_left", (TILES_SIZE,TILES_SIZE))
cooker_sprite = get_image("cooker", (TILES_SIZE,TILES_SIZE))
fridge_sprite = get_image("fridge", (TILES_SIZE,TILES_SIZE))
grass_sprite = get_image("grassMid", (TILES_SIZE,TILES_SIZE))
ladder_sprite = get_image("ladder_mid", (TILES_SIZE,TILES_SIZE))
ladderTop_sprite = get_image("ladder_top", (TILES_SIZE,TILES_SIZE))
poele_sprite = get_image("poele", (TILES_SIZE,TILES_SIZE))
redWall = get_image("redWall", (TILES_SIZE,TILES_SIZE))
table_sprite = get_image("table", (TILES_SIZE,TILES_SIZE))
swordFish_oicture_sprite = get_image("swordfish_picture", (TILES_SIZE,TILES_SIZE))
grassPicture_sprite = get_image("grass_picture", (TILES_SIZE,TILES_SIZE))

fires = [get_image_fire(f"fire{i}", ((TILES_SIZE), (TILES_SIZE))) for i in range(1,7)]
waterBucket = get_image_fire("water_bucket", (TILES_SIZE,TILES_SIZE))





class MovableObject(pg.sprite.Sprite):
    
    def __init__(self, x=0, y=0, image=None, tile_size=32, is_hard=True, is_liftable=False,
                 is_fire = False, gravity=0.75, has_gravity=False,is_container = False, map=None):
        super().__init__()
        
        self.tile_size = tile_size
        self.liftable = False
        if image == None:
            self.image = pg.Surface((tile_size,tile_size))
            if is_fire:
                self.image.fill((0,255,0))
            else:    
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
        self.is_fire = is_fire
        self.is_container = is_container
        self.is_liftable = is_liftable
        self.is_dirty = False
        
        # self.speedfact_x = 50
        # self.speedfact_y = 50
        
        self.map = map
        
        self.iteration = 0
        
        self.update_end()
    
    def update(self, dt):
        self.update_middle(dt)
        self.update_end(dt)
    
    
    def update_middle(self, dt=1):
        #Calcul la nouvelle position.
        self.pos.x += self.vel.x * dt * 3.1
        self.vel.x = round(self.vel.x * 0.85, 3)
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if (self.vel.x != 0 or self.has_gravity):
            self.vel.y += self.gravity
            self.pos.y += self.vel.y * dt * 50
            if (self.map.collide_block_with_tile(self, 'y')) == "S":
                self.has_gravity = False
            self.map.collide_block_with_tile(self, 'x')

                

                
    def update_end(self, dt=1):
        #Le reste mdr
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        self.iteration += 1
    
    def draw(self, screen, padding=(0,0)):
        screen.blit_cam(self.image, self.rect.move(padding))

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
        self.speedfact_x = 25
        self.speedfact_y = 45

class WaterBucket(Liftable):
    """
    Class for buckets and furnitures that can be lifted by the players
    """
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None):
        super().__init__(x, y, waterBucket, tile_size, map)
    
    def extinguish(self,fire_core):
        print("Extinction du feu")
        self.map.freeze(5)
        fire_core.kill()
        self.kill()

    def update_middle(self, dt=1):
        super().update_middle(dt=dt)
        fire_collided = self.map.collide_with_tile(self,self.map.fire_tiles)
        if(fire_collided[0]!=None):
            self.extinguish(fire_collided[0])

class Furniture(Liftable):
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None, value = 0):
        super().__init__(x, y, image, tile_size, map)
        self.is_saved = False
        self.value = value
    
    def get_saved(self):
        self.map.score += self.value
        print(self.map.score)
        self.is_saved = True
        self.liftable = False
    
    def update_middle(self,dt = 1):
        super().update_middle(dt=dt)
        if(self.pos.x > self.map.safe_zone and not self.is_saved):
            self.get_saved()


class Container(MovableObject):
    """
    Class for all furnitures that can be looted by the player
    """
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None):
        super().__init__(x, y, image, tile_size, is_hard=False, map=map,is_container = True)
        self.image.fill((48,32,212))

    def interact(self):
        self.map.score += R.randint(0,30)