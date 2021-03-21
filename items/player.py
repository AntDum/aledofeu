import pygame as pg
from items import movable_object
import os

TILES_SIZE = 32

def get_image(name, scale):
    return pg.transform.scale(pg.image.load(os.path.join("res",f"{name}.png")), scale)

player_sprite_left = [get_image(f"walk_left_{i}", ((TILES_SIZE*11)//17, (TILES_SIZE*17)//17)) for i in range(3)]
player_sprite_left.append(player_sprite_left[1])
player_sprite_right = [get_image(f"walk_right_{i}", ((TILES_SIZE*11)//17, (TILES_SIZE*17)//17)) for i in range(3)]
player_sprite_right.append(player_sprite_right[1])
player_sprite_idle = get_image("idle", ((TILES_SIZE*14)//17, (TILES_SIZE*17)//17))


class Player(movable_object.MovableObject):
    def __init__(self, x=0, y=0, speed=10, jump_force=15, gravity=0.75, tile_size=32, map=None):
        super().__init__(x,y,image=player_sprite_idle,tile_size=tile_size, gravity=0.75, has_gravity=True, map=map)
        self.speed = speed
        self.inventory = None
        self.jump_force = jump_force
        self.touch_ground = True
        self.last_push = -100
        self.looking_right = True

    def update(self, dt):
        self.vel.y += self.gravity * 50
        fact_x = 35
        fact_y = 50
        if self.inventory:
            fact_x = self.inventory.speedfact_x
            fact_y = self.inventory.speedfact_y

        self.get_keys(fact_x, fact_y)
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.x = self.pos.x
        self.map.collide_block_with_tile(self, 'x')
        self.rect.y = self.pos.y
        if (self.map.collide_block_with_tile(self, 'y')) == "S":
            self.touch_ground = True
        else:
            self.touch_ground = False

        if(self.inventory):
            padding_y = -1 * self.tile_size
            self.inventory.pos.x = self.pos.x
            self.inventory.pos.y = self.pos.y + padding_y
            self.inventory.update_end()


        super().update_end(dt)

    def draw(self, screen, dt):
        ite = self.iteration * dt * 10
        padding = self.tile_size*(4/17)
        if self.vel.x < 0:
            self.image = player_sprite_left[int(ite % 4)]
        elif self.vel.x > 0:
            self.image = player_sprite_right[int(ite % 4)]
        else:
            self.image = player_sprite_idle
            padding = self.tile_size*(2/17)

        if(self.inventory):
            self.inventory.draw(screen)
        super().draw(screen, (padding,0))


    def interact(self):
        """
        If the player is on a furniture and has nothing in his inventory, the furniture is removed from the map
        and placed in the inventory.
        """
        used_tile = pg.sprite.spritecollide(self, self.map.liftable_tiles, False)
        if(used_tile and used_tile[0].is_liftable):
            used_tile = used_tile[0]
            used_tile.kill()
            used_tile.is_dirty = True
            padding_y = -1 * self.tile_size
            self.inventory = used_tile
            self.inventory.pos.x = self.pos.x
            self.inventory.pos.y = self.pos.y + padding_y
            used_tile.has_gravity = False
            return True
        used_tile = pg.sprite.spritecollide(self, self.map.containers_tiles, False)
        if(used_tile and used_tile[0].is_container):
            used_tile[0].open()

    def drop(self):
        """
        If there is a furniture in the inventory, it's placed on the player position.
        """
        self.inventory.has_gravity = True
        self.inventory.vel.x = self.vel.x * 2
        self.map.add_tile(self.inventory)
        self.inventory = None


    def get_keys(self, fact_x, fact_y):
        """
        Gather key board input and applies it.
        """
        keys = pg.key.get_pressed()
        if(keys[pg.K_SPACE]):
            if (self.iteration-self.last_push > 8):
                self.last_push = self.iteration
                if(self.inventory):
                    self.drop()
                else:
                    self.interact()
        self.vel.x = (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * self.speed * fact_x
        # self.vel.y = (keys[pg.K_DOWN] - keys[pg.K_UP]) * self.speed
        if self.touch_ground:
            self.vel.y -= keys[pg.K_UP] * self.jump_force * fact_y
            if keys[pg.K_UP]:
                self.touch_ground = False
