import pygame.font
import os
import pygame as pg
pygame.font.init()
## TODO: Refaire ce qui touche à la fonction center et à la variable box_size, il y a des bugs. (Si les sous boites ne forment pas un bloc, center ne fonctionnera pas correctement.)
class TextBox:
    """
    FR: L'objet textBox est semblable aux boites de textes qu'on trouve sur Word ou GIMP2. Elle servent a ecrire du texte
        sur une fenêtre pygame.
    EN: textBos object is similar to text boxes that in Word or GIMP2. They are used to write text on a pygame window.
    """
# Méthodes d'initialisation et diverse==========================================
    def __init__(self,ID = "00",text = '',font = 'arial',font_size = 16,x_pos = 0,y_pos = 0, color = (255,255,255),italic = False,bold = False):
        """
        FR: Initialise une textBox avec 'text', qui peut être n'importe quelle variable, le contenu de la boite et font sa
            police. Par defaut, la police est arial-16, la boite est placee dans le coin superieur gauche et sera ecrit
            en blanc.
        EN: Initialize a textBox with text, which can be any type of variable, the text inside the box and font, it's font.
            By default, font is arial-16, the box is place on the left upper corner and will be printed in white.
        """
        self.ID = ID
        self.mother_box = None
        self.linked_boxes = []
        self.bold = bold
        self.italic = italic
        self.color = color
        self.fontName = font
        self.fontSize = font_size
        #print(pygame.font.get_fonts())
        self.font = pygame.font.SysFont(font,font_size)
        self.x = x_pos
        self.y = y_pos
        self.text = str(text)
        self.render()
        self.box_size = self.text_size

    def __str__(self):
        return(self.ID)


#Méthodes de modifications des éléments=========================================
    def change_text(self,text):
        """
        FR: Remplace le texte de la boite par text. Par defaut, genere un rendu.
        EN: Replace the box's text by text. By default, generate a new image.
        """
        self.text = str(text)
        return self

    def change_font_from_file(self,font = False,fontSize = False,color = (255,255,255)):
        """
        FR: Modifie la police de la boite depuis un fichier ressource.
        EN: Change the box's font from a ressource file.
        """
        if fontSize == False:
            fontSize = self.fontSize
        if font == False:
            font = self.fontName
        self.font = pygame.font.Font(os.path.join("Ressources",f"{font}.ttf"),fontSize)
        self.color = color
        self.render()
        return self

    def change_font(self,font = False,fontSize = False,switch_bold = False,switch_italic = False,color = (255,255,255)):
        """
        FR: Modifie la police de la boite depuis une police du systeme.
        EN: Change the box's font from system font.
        """
        if switch_bold:
            self.bold = not(self.bold)
        if switch_italic:
            self.italic = not(self.italic)
        if fontSize == False:
            fontSize = self.fontSize
        if font == False:
            font = self.fontName
        self.font = pygame.font.SysFont(font,fontSize,self.bold,self.italic)
        self.color = color
        self.render()
        return self

#Méthodes de création de rendu et d'affichage===================================
    def render(self):
        """
        FR: Genere un rendu actuel de la boite de texte et en calcule la taille.
        EN: Generate a render of the box and compute it's size.
        """
        self.score_text = self.font.render(self.text, 1,self.color)
        self.text_size = self.score_text.get_size()
        for box in self.linked_boxes:
            box.render()
        return self

    def print(self,window):
        """
        FR: Ecrit le contenu du dernier rendu a la position actuelle de la boite. Ne mets pas a jour la fenetre.
        EN: Write the last render on the current position of the box. Doesn't flip the window.
        """
        window.blit(self.score_text,(self.x,self.y))
        for box in self.linked_boxes:
            box.print(window)
        return self


#Méthodes de déplacement========================================================
    def center(self,window):
        """
        FR: Centre la boite dans la fenêtre.
        EN: Centre the box in the window.
        """
        window_size = window.get_size()
        box_size = self.text_size
        # print(box_size)
        self.move_to((window_size[0]-box_size[0])//2,(window_size[1]-box_size[1])//2)
        return self

    def move_to(self,x = 0,y = 0):
        """
        FR: Deplace le coin superieur gauche de la boite aux coordonnees x et y.
        EN: Moves the upper left corner of the box to the point x y.
        """
        for box in self.linked_boxes:
            box.move(x-self.x,y-self.y)
        self.x = x
        self.y = y
        return self

    def move(self,x = 0,y = 0):
        """
        FR: Decale la boite d'une distance x et y.
        EN: Moves the box by a distance x and y.
        """
        self.x += x
        self.y += y
        for box in self.linked_boxes:
            box.move(x,y)
        return self

    def stick_under_center(self,target):
        """
        FR: Place la boite en dessous de la boite target.
        EN: Place the box under the target box.
        """
        self.stick_under_left(target)
        self.move(x = (target.text_size[0]-self.text_size[0])//2)
        return self

    def stick_under_left(self,target):
        """
        FR: Colle la boite en dessous de la boite mère.
        EN: Stick the box under the mother box.
        """
        self.move_to(target.x,target.y+target.text_size[1])
        return self

    def stick_after(self,target):
        """
        FR: Colle la boite à la suite d'une autre boite. Bouger la boite principale bouge l'autre egalement.
            Recoller la boite à une autre boite supprime le premier lien.
        EN: Stick the box after an other box. Moving the main box moves the other too. Resticking the box to
            an other one deletes the first link.
        """
        self.move_to(target.x+target.text_size[0],target.y)
        return self


#Méthodes de liaisons===========================================================
    def link_to(self,mother):
        """
        FR: Lie la boite à la boite mother. Bouger la boite mother bougera l'autre également, l'inverse est faux.
            Relier la boite à une autre boite mère coupera ce lien. Plusieurs niveaux sont possibles.
        EN: Links the box to a mother box. Moving the mother box will move the other too.
            Relinking the box to another mother box will cut the link.
        """
        self.mother_box = mother
        self.mother_box.linked_boxes.append(self)
        box_width = max(self.box_size[0],mother.box_size[0])
        box_heigth = max(self.box_size[1],mother.box_size[1])
        return self

    def unlink(self):
        """
        FR: Coupe le lien avec la boite mère.
        EN: Unlink the box and the mother box.
        """
        if self.mother_box != None:
            self.mother_box.linked_boxes.remove(self)
            self.mother_box = None
        return self

    def print_links(self):
        print(f"Liens de la boite '{self}';")
        if self.mother_box != None:
            print(f"Boite mère trouvée. ID: {self.mother_box}")
        for box in self.linked_boxes:
            print(f"Boite liée trouvée. ID: {box}")
        return self
