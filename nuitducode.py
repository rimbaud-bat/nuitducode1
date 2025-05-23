import pyxel
import random
import math

class GameAssets:
    def __init__(self):
        # Dimensions des sprites
        self.joueur_width = 16
        self.joueur_height = 30
        self.bateau_width = 30
        self.bateau_height = 15
        self.projectile_size = 4
        self.bouton_width = 100
        self.bouton_height = 40

        # Couleurs
        self.couleur_eau = 5
        self.couleur_joueur = 7
        self.couleur_projectile = 10
        self.couleur_curseur = 8
        self.couleurs_bateaux = [8, 9, 10, 11, 12, 14, 15]
        self.couleur_bouton = 11
        self.couleur_bouton_hover = 10
        self.couleur_texte = 7
        self.couleur_commandes = 7
        self.couleur_timer = 7
        self.couleur_timer_alerte = 8  # Rouge pour les 10 dernières secondes

        pyxel.load("teme.pyxres")
        # Initialiser les images (à remplacer par de vrais sprites plus tard)
        self.init_images()

    def init_images(self):
        """Initialise les images pour le jeu"""
        # Cette méthode sera utilisée pour charger des images externes plus tard
        # Pour l'instant, nous définissons des fonctions de dessin simples
        pass

    def dessiner_joueur(self, x, y):
        """Dessine le joueur (canon) à la position spécifiée"""
        # Pour l'instant, un simple rectangle
        pyxel.blt(x - self.joueur_width//2, y - self.joueur_height//2,0,46,44,12,20)

    def dessiner_bateau(self, x, y, couleur):
        """Dessine un bateau à la position spécifiée"""
        pyxel.blt(x,y,1,0,0,29,24)

    def dessiner_projectile(self, x, y):
        """Dessine un projectile à la position spécifiée"""
        pyxel.circ(x, y, self.projectile_size//2, self.couleur_projectile)

    def dessiner_curseur(self, x, y):
        """Dessine le curseur à la position spécifiée"""
        pyxel.circ(x, y, 3, self.couleur_curseur)
        # Croix au centre du curseur
        pyxel.line(x-2, y, x+2, y, 7)
        pyxel.line(x, y-2, x, y+2, 7)

    def dessiner_eau(self):
        """Dessine l'arrière-plan d'eau"""
        pyxel.rect(0, 0, pyxel.width, pyxel.height, self.couleur_eau)

        # Ajouter quelques vagues (lignes horizontales plus claires)
        for y in range(20, pyxel.height, 40):
            pyxel.line(0, y, pyxel.width, y, 6)

    def dessiner_explosion(self, x, y, taille):
        """Dessine une explosion à la position spécifiée"""
        pyxel.circ(x, y, taille, 8)
        pyxel.circ(x, y, taille - 2, 10)
        pyxel.circ(x, y, taille - 4, 7)

    def dessiner_bouton(self, x, y, texte, hover=False):
        """Dessine un bouton avec du texte"""
        couleur = self.couleur_bouton_hover if hover else self.couleur_bouton

        # Rectangle du bouton
        pyxel.rect(x, y, self.bouton_width, self.bouton_height, couleur)

        # Bordure du bouton
        pyxel.rectb(x, y, self.bouton_width, self.bouton_height, self.couleur_texte)

        # Texte centré
        text_x = x + (self.bouton_width - len(texte) * 4) // 2
        text_y = y + (self.bouton_height - 5) // 2
        pyxel.text(text_x, text_y, texte, self.couleur_texte)

    def dessiner_commandes(self, x, y):
        """Dessine les instructions des commandes"""
        pyxel.text(x-150, y+20, "COMMANDES:", self.couleur_commandes)
        pyxel.text(x-90, y+20 , "Q: Quitter", self.couleur_commandes)
        pyxel.text(x-75, y+30 , "Clic gauche: Tirer", self.couleur_commandes)
        pyxel.text(x-35, y+20 , "Fleches: Deplacer", self.couleur_commandes)

    def dessiner_timer(self, x, y, temps_restant, temps_total=100):
        """Dessine le timer avec changement de couleur pour les 10 dernières secondes"""
        # Choisir la couleur en fonction du temps restant
        couleur = self.couleur_timer_alerte if temps_restant <= 10 else self.couleur_timer

        # Afficher le temps restant
        pyxel.text(x, y, f"TEMPS: {int(temps_restant)}", couleur)

    def dessiner_game_over(self):
            """Affiche l'écran de game over"""
            # Fond semi-transparent
            pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)
    
            # Texte "GAME OVER" centré
            texte = "non...pas comme ca"
            text_x = (pyxel.width - len(texte) * 4) // 2
            text_y = pyxel.height // 2
            pyxel.text(text_x, text_y, texte, 8)  # Rouge
    
        def dessiner_reussite(self):
            pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)
    
            # Texte "GAME OVER" centré
            texte = "on les à eu !!!"
            text_x = (pyxel.width - len(texte) * 4) // 2
            text_y = pyxel.height // 2
            pyxel.text(text_x, text_y, texte, 8)  # Rouge

class JeuBateaux:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        pyxel.init(256, 256, title="Jeu des Bateaux")

        # Charger les assets
        self.assets = GameAssets()

        # État du jeu: "accueil", "jeu" ou "game_over"
        self.etat = "accueil"

        # Position du bouton de démarrage
        self.bouton_x = (pyxel.width - self.assets.bouton_width) // 2
        self.bouton_y = pyxel.height // 2 + 20

        # Bateaux d'arrière-plan pour l'écran d'accueil
        self.bateaux_accueil = []

        # Position du joueur (en bas de l'écran)
        self.joueur_x = pyxel.width // 2
        self.joueur_y = pyxel.height - 20

        # Vitesse de déplacement du joueur
        self.joueur_vitesse = 3

        # Position du curseur
        self.curseur_x = 0
        self.curseur_y = 0

        # Liste des bateaux
        self.bateaux = []

        # Liste des projectiles
        self.projectiles = []

        # Liste des explosions
        self.explosions = []

        # Score
        self.score = 0

        # Timer
        self.temps_total = 15  # 100 secondes
        self.temps_restant = self.temps_total

        # Démarrer le jeu
        pyxel.run(self.update, self.draw)

    def creer_bateau_accueil(self):
        """Création aléatoire des bateaux pour l'écran d'accueil"""
        # Un bateau toutes les 20 frames (environ 0.66 seconde)
        if pyxel.frame_count % 20 == 0:
            nouveau_bateau = {
                "x": -30,  # Commence hors de l'écran à gauche
                "y": random.randint(20, pyxel.height - 50),
                "largeur": self.assets.bateau_width,
                "hauteur": self.assets.bateau_height,
                "vitesse": random.uniform(0.5, 1.5),  # Vitesse aléatoire
                "couleur": random.choice(self.assets.couleurs_bateaux)  # Couleur aléatoire
            }
            self.bateaux_accueil.append(nouveau_bateau)

    def deplacer_bateaux_accueil(self):
        """Déplacement des bateaux horizontalement et suppression s'ils sortent du cadre"""
        for bateau in self.bateaux_accueil[:]:
            # Déplacement horizontal
            bateau["x"] += bateau["vitesse"]

            # Suppression si le bateau sort de l'écran
            if bateau["x"] > pyxel.width:
                self.bateaux_accueil.remove(bateau)

    def verifier_bouton_start(self):
        """Vérifie si le bouton de démarrage est cliqué"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Vérifier si le clic est sur le bouton
            if (self.bouton_x <= self.curseur_x <= self.bouton_x + self.assets.bouton_width and
                self.bouton_y <= self.curseur_y <= self.bouton_y + self.assets.bouton_height):
                # Changer l'état du jeu
                self.etat = "jeu"
                # Réinitialiser les listes pour le jeu
                self.bateaux = []
                self.projectiles = []
                self.explosions = []
                self.score = 0
                # Réinitialiser le timer
                self.temps_restant = self.temps_total

    def est_sur_bouton(self):
        """Vérifie si le curseur est sur le bouton de démarrage"""
        return (self.bouton_x <= self.curseur_x <= self.bouton_x + self.assets.bouton_width and
                self.bouton_y <= self.curseur_y <= self.bouton_y + self.assets.bouton_height)

    def creer_bateau(self):
        """Création aléatoire des bateaux"""
        # Un bateau toutes les 30 frames (environ 1 seconde)
        if pyxel.frame_count % 30 == 0:
            # Les bateaux apparaissent à gauche de l'écran à une hauteur aléatoire
            # mais pas trop bas pour éviter qu'ils soient trop près du joueur
            nouveau_bateau = {
                "x": -30,  # Commence hors de l'écran à gauche
                "y": random.randint(20, pyxel.height // 2),
                "largeur": self.assets.bateau_width,
                "hauteur": self.assets.bateau_height,
                "vitesse": random.uniform(0.5, 2.0),  # Vitesse aléatoire
                "couleur": random.choice(self.assets.couleurs_bateaux)  # Couleur aléatoire
            }
            self.bateaux.append(nouveau_bateau)

    def deplacer_bateaux(self):
        """Déplacement des bateaux horizontalement et suppression s'ils sortent du cadre"""
        for bateau in self.bateaux[:]:
            # Déplacement horizontal
            bateau["x"] += bateau["vitesse"]

            # Suppression si le bateau sort de l'écran
            if bateau["x"] > pyxel.width:
                self.bateaux.remove(bateau)

    def deplacer_joueur(self):
        """Déplacement du joueur avec les touches du clavier"""
        # Déplacement vers la gauche avec la flèche gauche
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.joueur_x = max(self.joueur_x - self.joueur_vitesse, self.assets.joueur_width // 2)

        # Déplacement vers la droite avec la flèche droite
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.joueur_x = min(self.joueur_x + self.joueur_vitesse, pyxel.width - self.assets.joueur_width // 2)

    def tirer_projectile(self):
        """Envoie un projectile depuis le joueur vers la direction du curseur"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Calculer la direction vers le curseur
            dx = self.curseur_x - self.joueur_x
            dy = self.curseur_y - self.joueur_y

            # Normaliser le vecteur de direction
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx /= distance
                dy /= distance

            # Créer un nouveau projectile
            nouveau_projectile = {
                "x": self.joueur_x,
                "y": self.joueur_y,
                "dx": dx * 4,  # Vitesse horizontale
                "dy": dy * 4,  # Vitesse verticale
                "taille": self.assets.projectile_size
            }
            self.projectiles.append(nouveau_projectile)

    def deplacer_projectiles(self):
        """Déplacement des projectiles selon leur trajectoire et suppression s'ils sortent du cadre"""
        for projectile in self.projectiles[:]:
            # Déplacement selon la direction
            projectile["x"] += projectile["dx"]
            projectile["y"] += projectile["dy"]

            # Suppression si le projectile sort du cadre
            if (projectile["x"] < 0 or projectile["x"] > pyxel.width or
                projectile["y"] < 0 or projectile["y"] > pyxel.height):
                self.projectiles.remove(projectile)

    def verifier_collisions(self):
        """Vérifier les collisions entre projectiles et bateaux"""
        for projectile in self.projectiles[:]:
            for bateau in self.bateaux[:]:
                # Vérifier si le projectile touche un bateau
                if (projectile["x"] > bateau["x"] and
                    projectile["x"] < bateau["x"] + bateau["largeur"] and
                    projectile["y"] > bateau["y"] and
                    projectile["y"] < bateau["y"] + bateau["hauteur"]):

                    # Créer une explosion
                    self.explosions.append({
                        "x": projectile["x"],
                        "y": projectile["y"],
                        "taille": 10,
                        "duree": 10,
                        "frame": 0
                    })

                    # Supprimer le projectile et le bateau
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    if bateau in self.bateaux:
                        # Ajouter 20 points si la vitesse du bateau est supérieure à 1.5, sinon ajouter 10 points
                        if bateau["vitesse"] > 1.5:
                            self.score += 20
                        else:
                            self.score += 10
                        self.bateaux.remove(bateau)
                    break

    def mettre_a_jour_explosions(self):
        """Mettre à jour l'état des explosions"""
        for explosion in self.explosions[:]:
            explosion["frame"] += 1
            if explosion["frame"] >= explosion["duree"]:
                self.explosions.remove(explosion)

    def mettre_a_jour_timer(self):
        """Mettre à jour le timer et vérifier s'il est écoulé"""
        # Décrémenter le timer (30 FPS, donc 1/30 seconde par frame)
        self.temps_restant -= 1/30

        # Vérifier si le timer est écoulé
        if self.temps_restant <= 0:
            self.temps_restant = 0
            self.etat = "game_over"

    def update(self):
        """Mise à jour de l'état du jeu"""
        # Mettre à jour la position du curseur
        self.curseur_x = pyxel.mouse_x
        self.curseur_y = pyxel.mouse_y

        # Vérifier si la touche Q est pressée pour quitter
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.etat == "accueil":
            # Création et déplacement des bateaux d'arrière-plan
            self.creer_bateau_accueil()
            self.deplacer_bateaux_accueil()

            # Vérifier si le bouton de démarrage est cliqué
            self.verifier_bouton_start()

        elif self.etat == "jeu":
            # Création des bateaux
            self.creer_bateau()

            # Déplacement des bateaux
            self.deplacer_bateaux()

            # Déplacement du joueur
            self.deplacer_joueur()

            # Tirer un projectile
            self.tirer_projectile()

            # Déplacement des projectiles
            self.deplacer_projectiles()

            # Vérifier les collisions
            self.verifier_collisions()

            # Mettre à jour les explosions
            self.mettre_a_jour_explosions()

            # Mettre à jour le timer
            self.mettre_a_jour_timer()

        elif self.etat == "game_over":
            # Vérifier si le bouton de démarrage est cliqué pour recommencer
            self.verifier_bouton_start()

    def draw(self):
        """Affichage des éléments du jeu"""
        # Dessiner l'eau (fond bleu)
        self.assets.dessiner_eau()

        if self.etat == "accueil":
            # Dessiner les bateaux d'arrière-plan
            for bateau in self.bateaux_accueil:
                self.assets.dessiner_bateau(bateau["x"], bateau["y"], bateau["couleur"])

            # Dessiner le titre du jeu
            pyxel.text(pyxel.width//2- 55 , pyxel.height//4, "PREMIERE BATAILLE DE LEMNOS", 7)
            
            # Dessiner le bouton de démarrage
            hover = self.est_sur_bouton()
            self.assets.dessiner_bouton(self.bouton_x, self.bouton_y, "JOUER", hover)

            # Dessiner les commandes
            self.assets.dessiner_commandes(pyxel.width - 100, pyxel.height - 40)

            # Dessiner le curseur
            self.assets.dessiner_curseur(self.curseur_x, self.curseur_y)

        elif self.etat == "jeu":
            # Dessiner les bateaux
            for bateau in self.bateaux:
                self.assets.dessiner_bateau(bateau["x"], bateau["y"], bateau["couleur"])

            # Dessiner le joueur (canon)
            self.assets.dessiner_joueur(self.joueur_x, self.joueur_y)

            # Dessiner les projectiles
            for projectile in self.projectiles:
                self.assets.dessiner_projectile(projectile["x"], projectile["y"])

            # Dessiner les explosions
            for explosion in self.explosions:
                taille_actuelle = explosion["taille"] * (1 - explosion["frame"] / explosion["duree"])
                self.assets.dessiner_explosion(explosion["x"], explosion["y"], taille_actuelle)

            # Dessiner le curseur
            self.assets.dessiner_curseur(self.curseur_x, self.curseur_y)

            # Afficher le score
            pyxel.text(5, 5, f"SCORE: {self.score}", 7)

            # Afficher le timer
            self.assets.dessiner_timer(pyxel.width - 60, 5, self.temps_restant)



        elif self.etat == "game_over":
            # Dessiner les bateaux
            for bateau in self.bateaux:
                self.assets.dessiner_bateau(bateau["x"], bateau["y"], bateau["couleur"])

            # Dessiner le joueur (canon)
            self.assets.dessiner_joueur(self.joueur_x, self.joueur_y)

            # Afficher le score final
            pyxel.text(5, 5, f"SCORE FINAL: {self.score}", 7)

           pyxel.text(5, 5, f"SCORE FINAL: {self.score}", 7)
            if self.score > 120:
            # Afficher Game Over
                self.assets.dessiner_reussite()
                hover = self.est_sur_bouton()
                self.assets.dessiner_bouton(self.bouton_x, self.bouton_y, "On peut pas les laisser impunis...", hover)
            else :
                self.assets.dessiner_game_over()
            # Dessiner le bouton pour recommencer
                hover = self.est_sur_bouton()
                self.assets.dessiner_bouton(self.bouton_x, self.bouton_y, "Rattrapons les", hover)

            # Dessiner le curseur
            self.assets.dessiner_curseur(self.curseur_x, self.curseur_y)

# Lancer le jeu
if __name__ == "__main__":
    JeuBateaux()
