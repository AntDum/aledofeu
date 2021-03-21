import pygame as pg
from screen import Screen
from items import player
from map import map_from_file
from button import Button
import os

WIDTH = 800
HEIGHT = 600
FPS_MAX = 60
TILES_SIZE = 32

def replay():
    return False,True

def do_not_replay():
    return False,False

def main():
    pg.init()
    run = True
    screen = Screen(WIDTH, HEIGHT, TILES_SIZE)
    clock = pg.time.Clock()

    pg.display.set_caption("Aledofeu")
    background = pg.Surface([WIDTH, HEIGHT])
    background.fill((200,200,200))

    screen.background = background

    screen.blit(background, (0,0))


    map = map_from_file(os.path.join("niveaux", "lvl4.csv"), tile_size=TILES_SIZE)

    screen.set_size_tile(map.width_tile, map.height_tile)


    #Boucle du jeu
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

        #Création de l'écran de fin de partie
    #Création de l'écran de fin de partie
    is_in_menu = True
    new_game_wanted = False
    play_again = Button("Rejouer")
    play_again.move_to(200,200)
    play_again.change_action(replay)
    play_again.change_sprite(get_image("menu_button"),(300,300))
    quit_game = Button("Quitter")
    quit_game.change_action(do_not_replay)
    quit_game.move_to(100,100)
    while is_in_menu:
        play_again.draw(screen.surface)
        quit_game.draw(screen.surface)
        pg.display.flip()
        for event in pg.event.get(): # Recupere les events
            if event.type == pg.QUIT: # Ferme le jeu quand on quitte
                is_in_menu = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if(play_again.is_pos_in(mouse_pos)):
                    is_in_menu,new_game_wanted = play_again.get_pressed()
                if(quit_game.is_pos_in(mouse_pos)):
                    is_in_menu,new_game_wanted = quit_game.get_pressed()
    pg.quit() #quit le module pygame
    return new_game_wanted


playing = True
while playing:
    playing = main()
