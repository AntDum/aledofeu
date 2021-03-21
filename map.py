import pygame as pg
from items.player import Player
from items.movable_object import MovableObject,Container,Liftable,WaterBucket,Furniture,FixObject,FireCore
import random as R
import locate
import particleEffect
import os

pg.mixer.init()

def get_effect(name, volume):
    sound = pg.mixer.Sound(os.path.join("res","audio",f'{name}.wav'))
    sound.set_volume(volume)
    return sound

def get_music(name, volume):
    pg.mixer.music.load(os.path.join("res","audio",f'{name}.mp3'))
    return pg.mixer.music

sound_fire_extinguish = get_effect("drop_water", 0.5)
sound_throw = get_effect("throw", 0.5)
sound_destruction = get_effect("destruction", 0.5)
sound_explosion = get_effect("destruction", 0.5)
sound_jump = get_effect("jump", 0.2)
sound_land = get_effect("land", 0.1)
sound_reward = get_effect("reward", 0.25)
sound_tick = get_effect("tick", 0.05)

music_background = get_music("sound", 0.5)


tokens = {
    "60" : "inner_empty",
    "70" : "outer_empty",
    "0": "wall",
    "10": "ground destructible",
    "20": "wall",
    "30": "ground",
    "40": "wall destructible",
    "1" : "tab1", "11" : "tab2", "21" : "tab3",
    "31": "chaise","41" : "table", "51" : "etagere", 
    "2" : "seau",
    "3" : "lit", "13" : "coffre" , "23" : "four" , "33" : "frigo",
    "4" : "fireplace",
    "5" : "spawn player",
    "15" : "safer"
}


def map_from_file(filename, tile_size=32):
    """
    From a csv file, returns a map.
    """
    map_token = gen_level(filename)
    map = Map()
    map.height_tile = len(map_token)
    new_destroyable_pack = True #Boolean used to detect packs of burning floor.
    map.width_tile = len(map_token[0])
    for y, etage in enumerate(map_token):
        map.width_tile = max(map.width_tile, len(etage))

        for x, token in enumerate(etage):
            token = tokens[token]
            if token == "outer_empty": # Vide extérieur
                pass
            elif token == "inner_empty":
                new_destroyable_pack = True
            elif token == "ground":#Sol
                map.add_tile(FixObject(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "wall":#Murs
                map.add_tile(FixObject(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "wall destructible":#Murs cassables
                map.add_tile(FixObject(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "ground destructible": # Sol destructibles
                new_tile = FixObject(x,y,tile_size=tile_size,map=map)
                if(new_destroyable_pack):
                    map.destroyable_packages.append(pg.sprite.Group())
                    new_destroyable_pack = False
                map.destroyable_packages[-1].add(new_tile)
                map.add_tile(new_tile)

            elif token == "tab1": # Tableau tier 1
                map.add_tile(Furniture(x,y,tile_size=tile_size,map=map, kind = 10))
                new_destroyable_pack = True
            elif token == "tab2": # Tableau tier 2
                map.add_tile(Furniture(x,y,tile_size=tile_size,map=map, kind = 11))
                new_destroyable_pack = True
            elif token == "tab3": # Tableau tier 3
                map.add_tile(Furniture(x,y,tile_size=tile_size,map=map, kind = 12))
                new_destroyable_pack = True
            elif token == "chaise": # Tableau tier 3
                map.add_tile(Furniture(x,y,tile_size=tile_size,map=map, kind = 20))
                new_destroyable_pack = True
            elif token == "table": # Tableau tier 3
                map.add_tile(Furniture(x,y,tile_size=tile_size,map=map, kind = 21))
                new_destroyable_pack = True

            elif token == "lit": # Contenur
                map.add_tile(Container(x,y,tile_size=tile_size,map=map, kind=10))
                new_destroyable_pack = True
            elif token == "coffre": # Contenur
                map.add_tile(Container(x,y,tile_size=tile_size,map=map, kind=11))
                new_destroyable_pack = True
            elif token == "four": # Contenur
                map.add_tile(Container(x,y,tile_size=tile_size,map=map, kind=12))
                new_destroyable_pack = True
            elif token == "frigo": # Contenur
                map.add_tile(Container(x,y,tile_size=tile_size,map=map, kind=13))
                new_destroyable_pack = True

            elif token == "seau": # Seaux
                map.add_tile(WaterBucket(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "echelle": # échelles
                map.add_tile(Liftable(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "fireplace": # incendie
                map.add_tile(FireCore(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True

            elif token == "safer": # Point de depot
                map.add_tile(FixObject(x,y,tile_size=tile_size,map=map))
                new_destroyable_pack = True
                map.safe_zone = x*tile_size

            elif token == "spawn player": # Spawn player
                map.player.set_pos(x,y)
                new_destroyable_pack = True

    return map

def gen_level(filename):
    """Randomly places stairs in the level, each stair will be placed between two floor delimiters.
    """
    map_token = []
    with open(filename) as f:
        for line in f:
            map_token.append(line.strip().split(','))

    for j,line in enumerate(map_token):
        if('20' in line):
            left_wall = line.index('20')
            right_wall = line.index('20',left_wall+1)
            stair_pos = R.randint(left_wall+1,right_wall-5)
            line[stair_pos:stair_pos+4] = ['60','60','60','60']
            map_token[j-1][stair_pos:stair_pos+4] = ['60','60','60','60']
            map_token[j+3][stair_pos+1:stair_pos+3] = ['0','0']
    return map_token

class Map:
    def __init__(self, tile_size=32):
        self.countdown = 60
        self.countdown_locater = locate.TextBox(font_size = 150)
        self.score = 0
        self.score_locater = locate.TextBox(x_pos=0,y_pos=0)
        self.safe_zone = 0
        self.freeze_cooldown = 0
        self.tile_size = tile_size
        self.tiles = pg.sprite.Group()
        self.particles = []
        self.fire_tiles = pg.sprite.Group()
        self.liftable_tiles = pg.sprite.Group()
        self.containers_tiles = pg.sprite.Group()
        self.tiles_collider = pg.sprite.Group()
        self.destroyable_packages = []
        self.width_tile = 0
        self.height_tile = 0
        self.iteration = 0
        self.last_shake = -100
        self.player = Player(tile_size = tile_size, map=self)
        music_background.play()


    def freeze(self,lap):
        self.freeze_cooldown += lap

    def update(self, screen, dt):
        #Gestion du compteur
        if(self.freeze_cooldown > 0):
            self.freeze_cooldown -= dt
        else:
            if self.iteration % 2 == 0:
                self.play_effect("tick")
            self.countdown -= dt
            self.freeze_cooldown = 0
        if(round(self.countdown % 5,1) == 0):
            i = R.randint(0,len(self.destroyable_packages)-1)
            for tile in self.destroyable_packages[i]:
                tile.kill()
            self.last_shake = self.iteration

        #Update des éléments
        self.tiles.update(dt)
        self.player.update(dt)
        screen.update_camera(self.player)

        self.countdown_locater.change_text(str(int(self.countdown)))
        
        for particle in self.particles:
            particle.update(dt)
            if particle.has_finish:
                self.particles.remove(particle)
        

        if (self.last_shake - self.iteration) * dt > -10 * dt:
            screen.shake()

        self.iteration += 1

        self.score_locater.change_text(f"Score : {self.score}")
        self.score_locater.render()
        self.countdown_locater.render()
        self.countdown_locater.center(screen.surface).move(y=-240)
        self.countdown_locater.render()


    def add_tile(self, tile):
        self.tiles.add(tile)
        if(tile.is_hard):
            self.tiles_collider.add(tile)
        if(tile.is_fire):
            self.fire_tiles.add(tile)
        if(tile.is_container):
            self.containers_tiles.add(tile)
        if(tile.is_liftable):
            self.liftable_tiles.add(tile)


    def collide_block_with_tile(self, entity, dir):
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


    def collide_with_tile(self, entity, group):
        """[summary]

        Args:
            entity : Qui est testé
            group : Avec quel groupe

        Returns:
            tuple: (hit, dir) hit l'objet avec qui a eu une collision
                                dir la direction dans la quel il y a une collision
                        dir est une liste avec les directions
            (None, []) si pas de collision
        """
        hit_dir = []
        hits = pg.sprite.spritecollide(entity, group, False)
        if hits:
            hits = hits[0]
            if entity.vel.x > 0:
                hit_dir.append("E")
            elif entity.vel.x < 0:
                hit_dir.append("W")

            if entity.vel.y > 0:
                hit_dir.append("S")
            elif entity.vel.y < 0:
                hit_dir.append("N")
        else:
            hits = None
        return (hits, hit_dir)

    def draw(self, screen, dt):
        for sprite in self.tiles.sprites():
            sprite.draw(screen)
        self.player.draw(screen, dt)
        for particle in self.particles:
            particle.draw(screen)
        self.countdown_locater.print(screen)
        self.score_locater.print(screen)
    
    def add_particle_fire(self, x, y):
        self.particles.append(particleEffect.FireExplosion(x, y, size=self.tile_size//16).explode())

    def add_particle_smoke(self, x, y):
        self.particles.append(particleEffect.Smoke(x,y, size=self.tile_size//3).explode())
        
    def add_particle_firework(self, x, y):
        self.particles.append(particleEffect.FireWork(x,y, timer=0.5, life_time=1, 
                        missile_size=self.tile_size//4, particule_size=self.tile_size//16))
    def add_particle_land(self, x, y):
        self.particles.append(particleEffect.LandExplosion(x,y, life_time=0.5, size=self.tile_size//16).explode())
        
    def play_effect(self, effect):
        if effect == "jump":
            sound_jump.play()
        elif effect == "throw":
            sound_throw.play()
        elif effect == "destruction":
            sound_destruction.play()
        elif effect == "fire_extinguish":
            sound_fire_extinguish.play()
        elif effect == "explosion":
            sound_explosion.play()
        elif effect == "land":
            sound_land.play()
        elif effect == "reward":
            sound_reward.play()
        elif effect == "walk":
            pass
        elif effect == "tick":
            sound_tick.play()