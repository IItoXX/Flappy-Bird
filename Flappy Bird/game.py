import pygame as pg 
import sys, time
from bird import Bird
from pipe import Pipe
from pygame import mixer

pg.init()

class Game:
    def __init__(self):
        # Settings de la fenetres
        pg.mixer.init()  # Initialisation de Mixer pour les bruitages de fond
        self.width = 600 # Largeur de la fenetre 
        self.height = 760 # Hauteur de la fenetre
        # Redimensionner des images dans le jeux (Ajuster la taille )
        self.scale_factor=1.5


        self.win = pg.display.set_mode((self.width, self.height))  # Création de la fenetres de jeu de la taille spécifié 

        self.clock = pg.time.Clock() # Deux actions principale : Mesure le temps écoule avec le dernier appelle tick (entre chaque appel ), régule la vitesse de la boucle du jeux Frames per second

        self.move_speed = 250 # Régulation de la vitesse de déplacement du jeux (pour le sol qui se déplace )

        self.start_monitoring = False  #Booléan Qui sers a surveiller le passage de l'oiseau entre les tuyaux  et ajouter le score

        self.score = 0  # Défini le score sur 0 a chaque début de partie

        self.font = pg.font.Font("assets/font.ttf", 24) # Police d'écriture utiliser 

        self.score_text = self.font.render("Score : 0", True, (255,255,255))  #( Création du texte affichant le score en haut a gauche Avec la couleur )
        self.score_text_rect = self.score_text.get_rect(center =(100,30))     #( Sa crée un rectangle qui entoure le texte avec les coordonées)

        self.restart_text = self.font.render("Restart", True, (255,255,255))  # Pareil mais pour le bouton Restart se qui relance le jeux (Que graphique ici)
        self.restart_text_rect = self.restart_text.get_rect(center =(300,700))


        self.bird = Bird(self.scale_factor)  # Appelle la class bird.py et ajuste la taille de l'oiseau 

        # Ajoutez les sons pour les Bruitages de gains de point ou de battement des ailes 
        self.pipe_sound = pg.mixer.Sound("assets/sfx/point.mp3")
        self.death_sound = pg.mixer.Sound("assets/sfx/die.mp3",)
        self.flap_sound = pg.mixer.Sound("assets/sfx/flap.mp3")


        self.is_enter_pressed = False  # Bolean permettant de vérifier si une touche (espace ou entrer) est utiliser  ou non
        self.is_game_started = True  # Bolean permettant de vérifier l'etat du jeux  (ON, OFF)


        self.pipes=[]  # Stock les objets tuyaux qui apparaissent dans le jeu 
        self.pipe_generate_counter=71  # Variables initialiser et compteur pour déterminer quand générer de nouveaux tuyaux (decrémentation a chaque itération de la boucle quand elle atteint zero un nouveau tuyaux est générer)

        self.setupBackground()  # Initialisation du Fond de jeu 

        self.runMenu()  # Initialse l'interface du Menu (def)
        self.gameLoop() # Initialise La fonction principale du jeux 


    def runMenu(self):
        menu_font = pg.font.Font("assets/font.ttf", 48)   # écriture de police du Menu
        title_text = menu_font.render("Flappy Bird", True, (255, 255, 255))  # écriture du texte et sont positionnement et couleur
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))  # Centre le texte 

        start_button_font = pg.font.Font("assets/font.ttf", 36)  # Pareil police d'écriture et taille de la police
        start_button_text = start_button_font.render("Start A Game", True, (255, 255, 255))  # écriture 
        start_button_rect = start_button_text.get_rect(center=(self.width // 2, self.height // 2))  # centrer le texte 

        while True:  # Boucle principale 
            for event in pg.event.get(): 
                if event.type == pg.QUIT:  # Si le joueur ferme la fenètre tout s'arrete
                    pg.quit()  # Quitter l'interface
                    sys.exit() # Quitte le jeux/ fenetre plus rien ne tourne meme en fond
                if event.type == pg.MOUSEBUTTONUP: # Vérifie si le clique est enfoncé clique droit
                    if start_button_rect.collidepoint(pg.mouse.get_pos()):  # Vérifie les coordonées de la souris et de savoir si elle se trouve dans la fenetre de jeux 
                        return # sortir de la boucle 

            self.win.fill((0, 0, 0))  # Fond noir
            self.win.blit(title_text, title_rect)   # Déssiner le texte du titre sur la fenetre de jeu 
            pg.draw.rect(self.win, (0, 128, 255), start_button_rect)   # Cette ligne dessine un rectangle (bouton "Start") sur la surface de la fenêtre + couleur 
            self.win.blit(start_button_text, start_button_rect)  # Dessin du bouton start sur la surface du jeu 

            pg.display.update()  # Met a jours l'affichage pour tout les dessins effectuées sur la fenetre de jeu 
            self.clock.tick(60) # Controle la vitesse de la boucle pour limiter le nombre d"itération par seconde (économie des ressources process et jeux plus fluide visuellement)



    def gameLoop(self):
        last_time = time.time()  # Enregistre le temps actuel
        while True:  # boucle tant que 
            new_time = time.time()  # enregistre le temps actuel entre chaque itération de la boucle 
            dt = new_time - last_time  # Calcule la différence de temps, Cela donne le temps écoulé depuis la dernière itération de la boucle.
            last_time = new_time # met a jours la variable last time avec la valeur actuel et prépare le suvii du temps pour la prochaine itération 


            for event in pg.event.get():  # Attend l'évenement 
                if event.type == pg.QUIT: # Condition qui vérifie si l'evenement est en cours de traitement 
                    pg.quit() # Si l'événement "QUIT" est détecté, cette ligne appelle pg.quit(), qui est une fonction de Pygame permettant de quitter proprement le module Pygame
                    sys.exit() # Cette ligne utilise la fonction sys.exit() du module sys pour quitter complètement le programme. 
                if event.type==pg.KEYDOWN and self.is_game_started:  # vérifie sur la touche du clavier est enfoncé et que game started est True 
                    if event.key==pg.K_RETURN:  # Verifie si la touche enfoncé est entrer si c'est le cas alors on lance 
                        self.is_enter_pressed=True  # definie sur Vrai
                        self.bird.update_on=True  # Indicateur pour activer ou desactiver la mise a jours de l'oiseau les ailes par exemple 
                    if event.key==pg.K_SPACE and self.is_enter_pressed:  # Cette condition vérifie deux choses. Tout d'abord, elle vérifie si la touche enfoncée est la touche d'espace et si is enter pressed est vrai
                        self.bird.flap(dt)  # Action pour faire battre des ailes l'oiseau 

                if event.type == pg.MOUSEBUTTONUP:  # Condition verifie si le bouton de la souris est relaché (après un clic)
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()): # verifie les coordonées de la souris savoir si il est dans le bon rectangle pour relancer le jeux 
                        self.restartGame()  # Relancer le jeux 




            self.updateEverything(dt)  # met a jours la logique du jeux comme les mouvement de l'oiseau la génération de tuyaux avec le temps dt
            self.checkCollisions() # Appelle la methode checkcollisions de l'objet self  verifie si l'oiseau touche les tuyaux
            self.checkScore() # Verifie si l'oiseau a reussi a passer a travers un tuyaux et si oui Add +1 score 
            self.dessinDeTout()  # Comme c'est écrit il dessine tout l'arriere plan les tuyaux l'oiseau le score 
            pg.display.update()  # met a jours l'affichafe de tout les déssins
            self.clock.tick(60)  # Taux de raffraichissement de la boucle 

    def restartGame(self):
        self.score = 0 # réinitialise le score du jeu à zéro, indiquant que le joueur recommence avec un score de départ.
        self.score_text = self.font.render("Score : 0", True, (0,0,0))
        self.is_enter_pressed = False  # Cela indique que la touche "Enter" n'est plus considérée comme enfoncée, ce qui pourrait être utilisé pour contrôler certaines actions dans la boucle du jeu.
        self.is_game_started = True # indique que le jeu a recommencé 
        self.bird.resetPosition()  # remet l'oiseau a la case départ 
        self.pipes.clear() # efface tout les tuyaux de la cartes 
        self.pipe_generate_counter = 71  # Renitialise le compteur de générateur des tuyaux 
        self.bird.update_on = False  # Desactive la mise a jours de l'oiseau  pour arreter sont mouvement 


    def checkScore(self):  # est responsable de vérifier si l'oiseau a réussi à passer à travers les tuyaux et d'ajuster le score en conséquence
        if len(self.pipes) > 0:  # Verifie si la liste des tuyaux contient au moins 1 tuyaux 
            if (self.bird.rect.left > self.pipes[0].rect_down.left and  
            self.bird.rect.right < self.pipes[0].rect_down.right and not self.start_monitoring):  # ces deux lignes verifie trois chose : si la position horizontale gauche 
                # de l'oiseau est supérieur a la position horizontale gauche du bas du premier tuyau pareil pour la droite et l'oiseau n'a pas encore commencé a traverser les tuyaux

                self.start_monitoring = True  # Cela signifie que l'oiseau a deja commencé a traverser le tuyau
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring: # Si la position horizontale gauche de l'oiseau est supérieure
                # à la position horizontale droite du bas du premier tuyau Si la variable est True cela signifie que l'oiseau a déjà commencé à passer à travers les tuyaux


                self.start_monitoring = False #  le score est augmenté de 1, le texte du score est mis à jour, et un son de gain de score est joué.
                self.score += 1 # incrémentation a chaque fois que cette parti est executer sela add 1 au score
                self.score_text = self.font.render(f"Score : {self.score}", True, (255,255,255)) # met a jours le score
                self.pipe_sound.play()   # Son, gain de score +1



    def checkCollisions(self):   # responsable de savoir si il y a collisions entre l'oiseau et les tuyaux 
        if self.is_game_started is False:
            return
        
        if len(self.pipes):  # verifie si la liste des tuyau contient au moins 1 tuyau si il est vide c'est ignorer
            if self.bird.rect.bottom > 568: # Verifie si le bas de l'oiseau est en dessous de la position du sol qui est de 568 pixel
                self.bird.update_on = False # arret de la mise a jours de la position de l'oiseau
                self.is_enter_pressed = False  # la touche Entrer n'est plus considérée comme enfoncée
                self.is_game_started = False # le jeu n'est plus en cours et que le joueur a perdu.
                self.death_sound.play()
                
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)):  # verifie deux chose en mm temps si l'oiseau est en colision avec le tuyau inférieur ou du tuyau supérieur
                self.is_enter_pressed = False  # la touche Entrer n'est plus considérée comme enfoncée
                self.is_game_started = False  # le jeu n'est plus en cours et que le joueur a perdu.
                self.death_sound.play()
                

    def updateEverything(self,dt): # mise a jour des mouvement du sol et de l'oiseau dans le jeu
        if self.is_enter_pressed:
            # Mouvement du sol en continue 
            self.ground1_rect.x-=int(self.move_speed*dt)  # deplace horizontalement l'image du sol vers la gauche en fonction de la vitesse multiplié par le temps écoulé depuis la derniere itération
            self.ground2_rect.x-=int(self.move_speed*dt) # Pareil mais pour la deuxieme image 
            self.bird.update(dt)  # Mise a jours de la position de l'oiseau en fonction du temps écoulé 
            if self.ground1_rect.right<0:  # Verifie si la parti droite de la premiere image du sol depasse de la fenetre de jeu
                self.ground1_rect.x=self.ground2_rect.right # si la condition est vrai on remplace a la droite de la deuxieme image du sol
            if self.ground2_rect.right<0:  # pareil mais pour la deuxieme image du sol
                self.ground2_rect.x=self.ground1_rect.right

            #Génération des tuyaux
            if self.pipe_generate_counter>70:  # verifie si le compteur de tuyau a atteint une valeur supérieur a 70 elle est utiliser pour determiné quand gnerer un nouveau tuyau
                self.pipes.append(Pipe(self.scale_factor,self.move_speed)) # SI la condition est vrai il est temps de generer un nouveau tuyau on ajoute un nouveau objet a pipe et on le configure avec scale et move speed
                self.pipe_generate_counter=0  # Après avoir générerer un nouveau tuyau on renitialise le compteur 
                
            self.pipe_generate_counter+=1 #incrémentation du compteur de génération entre chaque itération de la boucle 

            
            for pipe in self.pipes: # itères a travers chaque objet dans la liste 
                pipe.update(dt) # Pour chaque tuyau sa met a jours la position du tuyau en fonction du temps écouler depuis la derniere itération d'ou le dt 
            

            if self.bird.is_flapping() and self.bird.time_since_last_flap == 0: # verifie que l'oiseau vole et si la velocité de l'oiseau est négative sa indique que l'oiseau vole vers le haut
                self.flap_sound.play()  # Son quand l'oiseau bat des ailes


            #Retire les tuyaux si il sorte du cadre du jeu de la fenetre
            if len(self.pipes)!=0: # verifie si la liste n'est pas vide 
                if self.pipes[0].rect_up.right<0: # verifie si la partie droite du rectangle du tuyau est supérieur au premier tuyau de la liste 
                    self.pipes.pop(0) # si cette condition est vrai sa veux dire que le premier tuyau est hors de l'ecran de jeu et donc on la supprime avec pop(0) de la liste 
                  




    def dessinDeTout(self): # responsable de tout les dessins du jeu
        self.win.blit(self.bg_img,(0,-300)) #dessine l'image de fond avec position 
        for pipe in self.pipes: # itère a travers tout les tuyau dans la liste 
            pipe.drawPipe(self.win) # dessine tout les tuyaux
        self.win.blit(self.ground1_img,self.ground1_rect) # dessine la premiere image du sol 
        self.win.blit(self.ground2_img,self.ground2_rect) # pareil pour la deuxieme image du sol
        self.win.blit(self.bird.image,self.bird.rect) # dessine l'image de l'oiseau 
        self.win.blit(self.score_text, self.score_text_rect) # dessine le score
        if not self.is_game_started: # verifie si le jeu n'a pas encore commencé  si c'est le cas texte de redem est déssiné 
            self.win.blit(self.restart_text, self.restart_text_rect) # le texte de redémarrage  est déssiné a la position demander 


    def setupBackground(self): # initialiser les élément graphique du fond et du sol

        self.bg_img = pg.image.load("assets/bg.png").convert() # Charge l'image du fond depuis le fichier et convertit sont format pour améliorer c'est performance
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor) # Redimensionne l'image du fond en fonction du facteur d'échelle  et permet d'ajuster sa taille
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor) # Charge l'image du sol depuis le fichier
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor) # Charge l'image du sol2 depuis le fichier
        self.ground1_rect = self.ground1_img.get_rect() #  Récupère le rectangle associé à la première image du sol
        self.ground2_rect = self.ground2_img.get_rect() #  Récupère le rectangle associé à la deuxieme image du sol

        self.ground1_rect.x = 0 # Initialise la position horizontale de la première image du sol à 0
        self.ground2_rect.x = self.ground1_rect.right # Initialise la position horizontale de la deuxième image du sol à la droite de la première image du sol
        self.ground1_rect.y = 568 # position verticale de la premiere image
        self.ground2_rect.y = 568 # pareil mais deuxieme image 

game = Game() # Marque l'execution du jeux 