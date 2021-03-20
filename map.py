import pygame as pg
from items.player import Player
from items.movable_object import MovableObject,Container,Liftable
import random as R
import locate

"""List des tokens
    
    0 = Vide
    1 = Sol
    10 = mur
    11 = mur destructible
    2 = Sol destructible
    3 = Recuprerable de categorie n
    4 = Conteneur
    5 = seau
    6 = echelle
    7 = coeur du feu
    8 = spawn player
    9 = point de placage pour secure les items
"""

def map_from_file(filename, tile_size=32):
    """
    From a csv file, returns a map.
    """
    map_token = gen_level(filename)
    map = Map()
    map.height_tile = len(map_token)
    map.width_tile = len(map_token[0])
    for y, etage in enumerate(map_token):
        map.width_tile = max(map.width_tile, len(etage))
        
        for x, token in enumerate(etage):         
            if token.startswith("0"): # Vide
                pass
            elif token.startswith("1"):
                if token == "1":
                    map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map))
                elif token == "10" or token =='12':
                    map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map, image=pg.Surface((tile_size, tile_size))))
                elif token == "11":
                    map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map))
            elif token.startswith("2"): # Sol
                map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map))        
            elif token.startswith("3"): # Sol destructible
                map.add_tile(Liftable(x,y,tile_size=tile_size,map=map))
            elif token.startswith("4"): # Contenur
                map.add_tile(Container(x,y,tile_size=tile_size,map=map))
            elif token.startswith("5"): # Seaux
                map.add_tile(Liftable(x,y,tile_size=tile_size,map=map))
            elif token.startswith("6"): # échelles
                map.add_tile(Liftable(x,y,tile_size=tile_size,map=map))
            elif token.startswith("7"): # incendie
                map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map))
            elif token.startswith("8"): # Spawn player
                map.player.set_pos(x,y)
            elif token.startswith("9"): # Point de depot
                map.add_tile(MovableObject(x,y,tile_size=tile_size,map=map))
    return map

def gen_level(filename):
    map_token = []
    with open(filename) as f:
        for line in f:
            map_token.append(line.strip().split(','))

    for j in range(len(map_token)):
        line = map_token[j]
        if('12' in line):
            left_wall = 0
            right_wall = 0
            i = 0
            while(line[i] != '12'):
                i+=1
            left_wall = i
            i+=1
            while(line[i] != '12'):
                i+=1
            right_wall = i
            stair_pos = R.randint(left_wall+1,right_wall-5)
            line[stair_pos:stair_pos+4] = ['0','0','0','0']
            map_token[j-1][stair_pos:stair_pos+4] = ['0','0','0','0']
            map_token[j+3][stair_pos+1:stair_pos+3] = ['2','2']
    return map_token

class Map:
    def __init__(self, tile_size=32):
        self.countdown = 60
        self.countdown_locater = locate.TextBox(font_size = 150)
        self.score = 0
        self.frozen_timer = False
        self.freeze_cooldown = 0
        self.tile_size = tile_size
        self.tiles = pg.sprite.Group()
        self.soft_tiles = pg.sprite.Group()
        self.tiles_collider = pg.sprite.Group()
        self.width_tile = 0
        self.height_tile = 0
        self.player = Player(tile_size = tile_size, map=self)
        

    def freezeCountdown(self,lap):
        self.frozen_timer = True
        self.freeze_cooldown = lap
    
    def update(self, screen, dt):
        if(self.freeze_cooldown > 0):
            self.freeze_cooldown -= dt
            if (self.frozen_timer):
                self.frozen_timer = False
        if(not self.frozen_timer):
            self.countdown -= dt

        self.tiles.update(dt)
        self.player.update(dt)
        screen.update_camera(self.player)
        self.countdown_locater.center(screen.surface).move(y=-250)
        self.countdown_locater.change_text(str(int(self.countdown)))

    
    def add_tile(self, tile):
        self.tiles.add(tile)
        if(tile.is_hard):
            self.tiles_collider.add(tile)
        else:
            self.soft_tiles.add(tile)


    def collide_with_tile(self, entity, dir):
        hit_dir = ""
        if dir == 'x':
            hits = pg.sprite.spritecollide(entity, self.tiles_collider, False)
            if hits:
                if entity.vel.x > 0:
                    entity.pos.x = hits[0].rect.left - entity.rect.width
                    hit_dir = "E"
                elif entity.vel.x < 0:
                    entity.pos.x = hits[0].rect.right
                    hit_dir = "W"
                entity.vel.x = 0
                entity.rect.x = entity.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(entity, self.tiles_collider, False)
            if hits:
                if entity.vel.y > 0:
                    entity.pos.y = hits[0].rect.top - entity.rect.height
                    hit_dir = "S"
                elif entity.vel.y < 0:
                    entity.pos.y = hits[0].rect.bottom
                    hit_dir = "N"
                entity.vel.y = 0
                entity.rect.y = entity.pos.y
        return hit_dir

    def draw(self, screen, dt):
        for sprite in self.tiles.sprites():
            sprite.draw(screen)
        self.player.draw(screen, dt)
        self.countdown_locater.print(screen)

