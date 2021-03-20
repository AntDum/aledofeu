import pygame as pg

class Screen:
    def __init__(self, w, h, tile_size=32):
        self.surface = pg.display.set_mode((w,h)) # définit l'écran
        self.camera = pg.Rect(0,0,w,h)
        self.blit = self.surface.blit # crée un raccourci
        self.background = None
        self.width = w
        self.height = h
        self.tile_size = tile_size
        self.amount_x_tile = 0
        self.amount_y_tile = 0
        
    def get_size(self):
        return (self.width,self.height)
    
    def draw_grid(self):
        for x in range(0, self.width, self.tile_size):
            pg.draw.line(self.surface, (181,181,181), (x,0), (x,self.height))
        for y in range(0, self.height, self.tile_size):
            pg.draw.line(self.surface, (181,181,181), (0,y), (self.width,y))

    def set_size_tile(self, w, h):
        self.amount_x_tile = w
        self.amount_y_tile = h
        
    def draw_background(self, rect):
        return self.blit(self.background, rect, rect)
    
    def background_cam(self, rect):
        return self.draw_background(rect.move(self.camera.topleft))

    def blit_cam(self, image, rect):
        return self.blit(image, rect.move(self.camera.topleft))
    
    def update_camera(self, target):
        x = -target.rect.x + self.width//2
        y = -target.rect.y + self.height//2

        x = min(0, x)
        y = min(0, y)
        
        width_map = self.amount_x_tile*self.tile_size
        height_map = self.amount_y_tile*self.tile_size

        x = max(-(width_map - self.width), x)
        y = max(-(height_map - self.height), y)

        self.camera.x = x
        self.camera.y = y