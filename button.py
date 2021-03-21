import locate
import pygame as pg
pg.init()

class Button:

    def __init__(self,name = 'Option sans nom'):
        self.name = name
        self.text_box_name = locate.TextBox(text = name,font_size = 16,color = (0,0,0))
        self.text_shift = (0,0)
        self.sprite = None
        self.area = pg.Rect((0,0),self.text_box_name.text_size)
        self.x = 0
        self.y = 0
        self.shift = (0,0)
        self.action = print
        self.parameters = "Bouton pressé"

#Méthodes de modifications graphiques===========================================
    def move_text(self,shift):
        self.text_shift = shift
        self.text_box_name.move(shift[0],shift[1])

    def center_text(self):
        self.move_text(((self.area.width-self.text_box_name.text_size[0])//2,(self.area.height-self.text_box_name.text_size[1])//2))

    def change_action(self,f,para = None):
        """
        FR: Associe une action au bouton. La fonction f doit accepter une liste
            (para). Au besoin, on peut définir une fonction intermédiaire.
        EN: Associate an action to the button. The function needs to take a list
            (para). If needed, an intermediate function can be written.
        """
        self.action = f
        self.parameters = para

    def change_sprite(self,sprite,scale = False, shift = 0):
        """
        FR: Change le sprite du bouton avec le décalage et l'échelle souhaitée.
            Si aucune échelle n'est spécifiée, le sprite sera mis à la même
            échelle que la boite de texte. La hitbox est automatiquement mise à jour.
        """
        if scale:
            self.sprite = pg.transform.scale(sprite,(scale))
        else:
            self.sprite = pg.transform.scale(sprite,(self.text_box_name.text_size[0],self.text_box_name.text_size[1]))
        self.shift = shift
        self.area = self.sprite.get_rect()

    def change_font(self,font = 'Calibri',size = 16, color = (0,0,0),fromFile = False):
        if fromFile:
            self.text_box_name.change_font_from_file(font,fontSize = size, color = color)
        else:
            self.text_box_name.change_font(font,fontSize = size, color = color)

#Méthodes de rendu et impression================================================
    def render(self):
        self.text_box_name.render()

    def draw(self,window):
        if self.sprite == None:
            pg.draw.rect(window,(0,0,0),self.area)
        else:
            window.blit(self.sprite,(self.x+self.shift[0],self.y+self.shift[1]))
        self.text_box_name.print(window)

#Méthodes de déplacement et autres==============================================
    def is_pos_in(self,pos):
        return self.area.collidepoint(pos)

    def move_to(self,x,y):
        self.move(x-self.x,y-self.y)

    def move(self,x,y):
        self.x += x
        self.y += y
        self.text_box_name.move(x,y)
        self.area = self.area.move(self.x-self.area.x+self.shift[0],
            self.y-self.area.y+self.shift[1])

    def get_pressed(self):
        print("Hey")
        if self.parameters:
            self.action(self.parameters)
        else:
            return self.action()
