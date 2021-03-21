import pygame as pg
import os
import random as R

TILES_SIZE = 32

def get_image(name, scale):
    return pg.transform.scale(pg.image.load(os.path.join("res","Tile",f"{name}.png")), scale)

def get_image_fire(name, scale):
    return pg.transform.scale(pg.image.load(os.path.join("res","fire",f"{name}.png")), scale)

def get_tile(name):
    return get_image(name, (TILES_SIZE,TILES_SIZE))

wall_sprite = get_tile("Wall")
woodBackGround_sprite = get_tile("Wood_backGround")
chairLeft_sprite = get_tile("chair_left")
chairRight_sprite = get_tile("chair_right")
table_sprite = get_tile("table")
bed_sprite = get_tile("bed_picture")
cooker_sprite = get_tile("cooker")
fridge_sprite = get_tile("fridge")
grass_sprite = get_tile("grassMid")
shelf_sprite = get_tile("shelf")
ladder_sprite = get_tile("ladder_mid")
ladderTop_sprite = get_tile("ladder_top")
poele_sprite = get_tile("poele")
red_wall_sprite = get_tile("redWall")
#Picture
swordFish_picture_sprite = get_tile("swordfish_picture")
grassPicture_sprite = get_tile("grass_picture")
shipPicture_sprite = get_tile("ship")
mountainPicture_sprite = get_tile("mountain")
flowerPicture_sprite = get_tile("flower_pot")

fires_sprite = [get_image_fire(f"fire{i}", ((TILES_SIZE), (TILES_SIZE))) for i in range(1,7)]
waterBucket_sprite = get_image_fire("water_bucket", (TILES_SIZE,TILES_SIZE))



class MovableObject(pg.sprite.Sprite):

    def __init__(self, x=0, y=0, image=None, tile_size=32, is_hard=True, is_liftable=False,
                 is_fire = False, gravity=0.75, has_gravity=False,is_container = False, map=None):
        super().__init__()

        self.tile_size = tile_size
        if image == None:
            self.image = pg.Surface((tile_size,tile_size))
            self.image.fill((0,255,0))
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
        self.is_ladder=False
        self.is_dirty = False

        self.particle = None
        # self.speedfact_x = 50
        # self.speedfact_y = 50

        self.map = map

        self.iteration = 0

        self.update_end()

    def kill(self):
        if self.particle != None:
            self.particle.has_finish = True
        super().kill()

    def update(self, dt):
        self.update_middle(dt)
        self.update_end(dt)


    def update_middle(self, dt=1):
        #Calcul la nouvelle position.
        self.pos.x += self.vel.x * dt * 2.5
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if (self.vel.x != 0 or self.has_gravity):
            self.vel.y += self.gravity
            self.pos.y += self.vel.y * dt * 35
            if (self.map.collide_block_with_tile(self, 'y')) == "S":
                self.has_gravity = False
                self.vel.x = round(self.vel.x * 0.80, 3)
            else:
                self.vel.x = round(self.vel.x * 0.91, 3)
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

    def use(self):
        pass


class Liftable(MovableObject):
    """
    Class for buckets and furnitures that can be lifted by the players
    """
    def __init__(self, x=0, y=0, image=None, tile_size=32, map=None):
        super().__init__(x, y, image=image,tile_size=tile_size, is_hard=False, is_liftable=True, map=map)
        self.speedfact_x = 25
        self.speedfact_y = 50

class WaterBucket(Liftable):
    """
    Class for buckets and furnitures that can be lifted by the players
    """
    def __init__(self, x=0, y=0, tile_size=32, map=None):
        super().__init__(x, y, image=waterBucket_sprite, tile_size=tile_size, map=map)

    def extinguish(self,fire_core):
        # print("Extinction du feu")
        self.map.freeze(10)
        fire_core.kill()
        self.kill()
        self.map.add_particle_smoke(fire_core.rect.centerx, fire_core.rect.centery)
        self.map.play_effect("fire_extinguish")

    def update_middle(self, dt=1):
        super().update_middle(dt=dt)
        fire_collided = self.map.collide_with_tile(self,self.map.fire_tiles)
        if(fire_collided[0]!=None):
            self.extinguish(fire_collided[0])


class Furniture(Liftable):
    def __init__(self, x=0, y=0, tile_size=32, map=None, kind = 1):
        self.is_saved = False
        if kind == 10: # Tableau tier 1
            self.value = 5
            if R.random() > 0.5:
                sprite = swordFish_picture_sprite
            else:
                sprite = grassPicture_sprite

        elif kind == 11: # Tableau tier 2
            self.value = 10
            if R.random() > 0.5:
                sprite = mountainPicture_sprite
            else:
                sprite = flowerPicture_sprite
        elif kind == 12: # Tableau tier 3
            self.value = 40
            sprite = shipPicture_sprite
        elif kind == 20: # Chaise gauche
            self.value = 5
            sprite = chairLeft_sprite
        elif kind == 21: # Chaise droite
            self.value = 5
            sprite = chairRight_sprite
        elif kind == 22: # Table
            self.value = 20
            sprite = table_sprite
        elif kind == 23:
            self.value = 30
            sprite = shelf_sprite
        else:
            sprite = None
            self.value = 0
        super().__init__(x, y, image=sprite, tile_size=tile_size, map=map)

    def get_saved(self):
        self.map.score += self.value
        self.is_saved = True
        self.liftable = False
        self.map.play_effect("reward")
        self.map.add_particle_reward(self.rect.centerx, self.rect.centery)
        self.kill()

    def update_middle(self,dt = 1):
        super().update_middle(dt=dt)
        fire_collided = self.map.collide_with_tile(self,self.map.fire_tiles)
        if(fire_collided[0]!=None):
            self.kill()
            self.map.add_particle_fire(self.rect.centerx, self.rect.centery)
            self.map.play_effect("destruction")

        if(self.pos.x > self.map.safe_zone and not self.is_saved):
            self.get_saved()


class Container(MovableObject):
    """
    Class for all furnitures that can be looted by the player
    """
    def __init__(self, x=0, y=0, tile_size=32, map=None, kind=0):
        if kind == 10: # lit
            self.value = 5
            sprite = bed_sprite
        elif kind == 11: # lit
            self.value = 10
            sprite = bed_sprite
        elif kind == 12: # cooker
            self.value = 40
            sprite = cooker_sprite
        elif kind == 13: # frigo
            self.value = 5
            sprite = fridge_sprite
        else:
            self.value = 0
            sprite = None
        super().__init__(x, y, image=sprite,tile_size=tile_size, is_hard=False, map=map, is_container=True)

    def open(self):
        r = R.random()
        if r > 0.3:
            if r >= 0.8:
                self.map.play_effect("firemen_siren")
                self.map.freeze(30)
            else:
                self.map.play_effect("reward")
                self.map.score += R.randint(5,25)
            self.map.add_particle_firework(self.rect.centerx, self.rect.bottom)
        self.kill()

class FixObject(MovableObject):
    def __init__(self, x=0, y=0, tile_size=32, map=None, kind=0):
        image = None
        is_hard = True
        if kind == 0:
            image = wall_sprite
        elif kind == 2:
            image = red_wall_sprite
        elif kind == 1:
            image = woodBackGround_sprite
            is_hard = False
        super().__init__(x,y, image=image, tile_size=tile_size, map=None, is_hard=is_hard)


class FireCore(MovableObject):
    def __init__(self, x=0, y=0, tile_size=32, map=None):
        super().__init__(x,y, image=fires_sprite[0], tile_size=tile_size, map=None, is_hard=False, is_fire=True)

    def update(self, dt):
        self.update_middle()
        ite = self.iteration * dt * 10
        self.image = fires_sprite[int(ite % 6)]
        self.update_end()


class Ladder(Liftable):
    def __init__(self, x=0, y=0, tile_size=32, map=None, item=True):
        super().__init__(x, y, image=ladder_sprite, tile_size=tile_size, map=map)
        if item == False:
            self.is_liftable=False
            self.is_ladder=True

    def use(self):
        self.map.add_ladder(self.pos.x, self.pos.y)
        self.kill()
        self.liftable = False
        # self.map.play_effect("reward")
        # self.map.add_particle_reward(self.rect.centerx, self.rect.centery)

    def update_middle(self,dt = 1):
        super().update_middle(dt=dt)
        fire_collided = self.map.collide_with_tile(self,self.map.fire_tiles)
        if(fire_collided[0]!=None):
            self.kill()
            self.map.add_particle_fire(self.rect.centerx, self.rect.centery)
            self.map.play_effect("destruction")
