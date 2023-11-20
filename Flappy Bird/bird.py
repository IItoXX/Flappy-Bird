import pygame as pg

class Bird(pg.sprite.Sprite):  # represente l'oiseau dans le jeu 
    def __init__(self,scale_factor):
        super(Bird,self).__init__()
        self.img_list=[pg.image.load("assets/birdup.png").convert_alpha(),
                        pg.image.load("assets/birddown.png").convert_alpha()]  # liste des deux images 1 pour la position haut et l'autre bas
    
        
        self.image_index=0 # Indice utiliser pour selectionner l'image actuelle de l'oiseau a afficher
        self.image=self.img_list[self.image_index] 
        self.rect=self.image.get_rect(center=(100,100)) # Un rectangle associé à l'image de l'oiseau. Il est utilisé pour déterminer la position et les collisions de l'oiseau
        self.y_velocity=0 # vitesse verticale de l'oiseau qui est affecté a la gravité et le mouvement des ailes 
        self.gravity=10 #  La force de gravité appliquée à l'oiseau, provoquant un déplacement vers le bas définis sur 10
        self.flap_speed = 250 # La vitesse à laquelle l'oiseau "flap", c'est-à-dire bat des ailes vers le haut
        self.anim_counter = 0 # Un compteur utilisé pour animer les ailes de l'oiseau
        self.update_on = True # Un indicateur qui contrôle si la mise à jour de l'oiseau est activée. Il est utilisé pour gérer l'état du jeu
        self.flap_cooldown = 0.5 # temps entre chaque battement d'ailes 
        self.time_since_last_flap = 0 # Le temps écoulé depuis le dernier battement d'ailes

    def is_flapping(self):
        return self.y_velocity < 0  # renvoi true si la vitesse verticale de l'oiseau est négative indiquant que l'oiseau bat des ailes vers le haut si la vitesse est positive ou nulle FALSE


    def update(self, dt): # responsable de mettre a jours la position de l'oiseau
        if self.update_on: # vérifie si la mise à jour de l'oiseau est activée si false alors l'oiseau reste immobile
            self.applyGravity(dt) # Appelle la méthode applyGravity pour appliquer la gravité à la vitesse verticale de l'oiseau. La gravité tire l'oiseau vers le bas, modifiant sa position verticale
            self.playAnimation() # anime les ailes de l'oiseau ce qui inclue le changement d'image pour simuler le mouvement de l'aile


        self.time_since_last_flap += dt # stocke la quantité totale de temps écoulé depuis le dernier battement d'ailes




        if self.rect.y<=0 and self.flap_speed==250: # si la position verticale de l'oiseau est inférieur ou égale a zero et la vitesse de battement est égale a 250 alors l'oiseau monte
            self.rect.y=0 # la position verticale est fixé a zero ce qui le maintient en haut
            self.flap_speed=0 # la vitesse de bttement d'aile est reduite a zero se qui l'empeche de monter hors du cadre
            self.y_velocity=0 # La vitesse verticale de l'oiseau est également réduite a zero pour arrter les mouvement verticale
        elif self.rect.y>0 and self.flap_speed==0: # Si a position verticale de l'oiseau est supérieur a zero et la vitesse de battement aussi alors l'oiseau est entrain de déscendre 
            self.flap_speed=250 # la vitesse de battement est renitialiser a 250 et sa lui permet de pouvoir remonter 

        if self.time_since_last_flap >= self.flap_cooldown: # verifie le temps écoulé depuis le dernier battement d'ailes est supérieur ou égal au temsp de recharge défini 
                if pg.key.get_pressed()[pg.K_SPACE]:  # verifie si la touche espace est enfoncé 
                    self.flap(dt) # appelle la methode flap pour fire voler l'oiseau
                    self.time_since_last_flap = 0 # renitialise le temps écouler depuis le derniere battement a zero et redemarre le compte a rebours pour le prochain battement d'aile


    def applyGravity(self,dt): # c'est se qui permet d'appliquer la gravité avec une formule de zinzin de l'espace
        self.y_velocity+=self.gravity*dt  # ajoute la vitesse verticale actuelle de l'oiseau y.velocity le produit de la gravité par le temps écoulé depuis la derniere itérations de la boucle du jeu
        # Cela simule l'effet de la gravité, car la vitesse verticale de l'oiseau augmente progressivement vers le bas
        self.rect.y+=self.y_velocity  # met à jour la position verticale de l'oiseau en ajoutant sa vitesse verticale actuelle à sa position actuelle

    def flap(self,dt): # mouvement vers le haut de l'oiseau
        self.y_velocity=-self.flap_speed*dt # la vitesse verticale de l'oiseau a une valeur négative ou égale a la vitesse de battement d'aile qui est multiplié par le temps écouler 

    def playAnimation(self):  # Gestion d'animation de l'oiseau alterne deux image se qui donne l'effet de battement d'ailes
        if self.anim_counter==5: # compteur d'animation atteint 5 
            self.image=self.img_list[self.image_index] # si la condition est vrai alors sa change l'image actuelle de l'oiseau en utilisant l'index d'image actuelle

            if self.image_index==0: self.image_index=1 # permet de passer d'une image a l'autre a chaque changement d'animation
            else: self.image_index=0 
            self.anim_counter=0 # après avoir fait le changement d'image le compteur d'animation est renitialiset a 0 et va re compter a 5
        
        self.anim_counter+=1  # incrémente le compteur d'animation

    def resetPosition(self):  # renitialise la position de l'oiseau
        self.rect.center = (100,100)  #le replace au coordonée 100 100
        self.y_velocity = 0  # met la velocité verticale a zero en attendant la touche enter qui soit presser
        self.anim_counter = 0  # remet a zero le compteur d'animation 