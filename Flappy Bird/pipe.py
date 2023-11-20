import pygame as pg
from random import randint


class Pipe:
    def __init__(self,scale_factor,move_speed):
        self.img_up=pg.transform.scale_by(pg.image.load("assets/pipeup.png").convert_alpha(),scale_factor) # Charge l'image du tuyau supérieur depuis le fichier
        self.img_down=pg.transform.scale_by(pg.image.load("assets/pipedown.png").convert_alpha(),scale_factor) # Charge l'image du tuyau inférieur depuis le fichier
        self.rect_up=self.img_up.get_rect() # Crée un rectangle associé à l'image du tuyau supérieur
        self.rect_down=self.img_down.get_rect() # Crée un rectangle associé à l'image du tuyau inférieur
        self.pipe_distance= randint(150, 200) # représente la distance entre les deux tuyaux
        self.rect_up.y=randint(250,520) # position verticale du rectangle du tuyau supérieur avec une valeur aléatoire entre 250 et 520
        self.rect_up.x=600  # position horizontale du rectangle du tuyau supérieur
        self.rect_down.y=self.rect_up.y-self.pipe_distance-self.rect_up.height # position verticale du rectangle du tuyau inférieur de manière à maintenir la distance verticale entre les deux tuyaux
        self.rect_down.x=600 # Initialise la position horizontale du rectangle du tuyau inférieur
        self.move_speed=move_speed # la vitesse de déplacement du tuyau avec la valeur fournie par le paramètre
    
    def drawPipe(self,win): # dessiner les images du tuyau supérieur et inferieur la la fenetre
        win.blit(self.img_up,self.rect_up) # Dessine l'image du tuyau supéreiru sur la fenetre la pos est determiner par le rectangle associé au tuyau supérieur
        win.blit(self.img_down,self.rect_down) # pareil mais pour le rectangle inférieur
    
    def update(self,dt):  # met a jours la position horizontale des rectangles associé au tuyau infé et supé en fonction du temps écouler 
        self.rect_up.x-=int(self.move_speed*dt) # Réduit la position horizontale du rectangle du tuyau supérieur en fonction de la vitesse de déplacement du tuyau sa deplace le tuyau supérieur vers la gauche en gros 
        self.rect_down.x-=int(self.move_speed*dt) # pareil réduit la position horizontale du rectangle du tuyau inférieur en fonction de la vitesse de déplacement du tuyau