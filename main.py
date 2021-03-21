import pygame as pg
from screen import Screen
from items import player
from map import map_from_file
import os

WIDTH = 800
HEIGHT = 600
FPS_MAX = 60
TILES_SIZE = 32


def main():
    pg.init()

    screen = Screen(WIDTH, HEIGHT, TILES_SIZE)
    clock = pg.time.Clock()

    pg.display.set_caption("Aledofeu")
    background = pg.Surface([WIDTH, HEIGHT])
    background.fill((200,200,200))

    screen.background = background

    screen.blit(background, (0,0))

    pg.display.flip()

    map = map_from_file(os.path.join("niveaux", "lvl4.csv"), tile_size=TILES_SIZE)

    screen.set_size_tile(map.width_tile, map.height_tile)


    #Boucle du jeu
    run = True
    while run:
        dt = clock.tick(FPS_MAX) / 1000 # connait le delta time entre les iterations
        fps = round(dt*(FPS_MAX**2),2) # connait les fps

        for event in pg.event.get(): # Recupere les events
            if event.type == pg.QUIT: # Ferme le jeu quand on quitte
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pass

        pg.display.set_caption(str(round(map.countdown, 3)))
        # pg.display.set_caption(str(fps))

        #update
        map.update(screen, dt)

        #draw
        # pg.display.update(map.draw(screen))
        screen.blit(background, (0,0))
        map.draw(screen, dt)
        # screen.draw_grid()
        if map.countdown < 0:
            run = False

        #update screen
        pg.display.flip()


    pg.quit() #quit le module pygame


main()
