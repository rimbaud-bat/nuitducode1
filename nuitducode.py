import pyxel
import random

class JeuBateaux:
    def __init__(self):
        pyxel.init(256, 256, title="Jeu des Bateaux")

        # Charger les ressources depuis le fichier theme.pyxres
        pyxel.load("theme.pyxres")

        self.bateaux = []
        self.vitesse = 1

        # Initialiser la position des bateaux
        for i in range(3):
            self.bateaux.append({
                "x": -i * 60,
                "y": 30,
                "largeur": 40,
                "hauteur": 20
            })

        # Position du curseur
        self.curseur_x = 0
        self.curseur_y = 0

        # Liste des ennemis
        self.ennemis_liste = []

        # Liste des projectiles
        self.projectiles_liste = []

        pyxel.run(self.update, self.draw)

    def ennemis_creation(self):
        """Création aléatoire des ennemis"""
        # Un ennemi par seconde
        if pyxel.frame_count % 30 == 0:
            self.ennemis_liste.append([0, random.randint(20, pyxel.height - 20)])

    def ennemis_deplacement(self):
        """Déplacement des ennemis horizontalement et suppression s'ils sortent du cadre"""
        for ennemi in self.ennemis_liste[:]:
            ennemi[0] += 1
            if ennemi[0] > pyxel.width:
                self.ennemis_liste.remove(ennemi)

    def tirer_projectile(self):
        """Envoie un projectile depuis le curseur"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.projectiles_liste.append([self.curseur_x, self.curseur_y, self.curseur_y])  # Stocker la position y de la cible

    def deplacer_projectiles(self):
        """Déplacement des projectiles et suppression s'ils sortent du cadre"""
        for projectile in self.projectiles_liste[:]:
            # Déplacement vertical vers la position y de la cible
            if projectile[1] < projectile[2]:
                projectile[1] += 2
            elif projectile[1] > projectile[2]:
                projectile[1] -= 2

            # Suppression si le projectile atteint la cible ou sort du cadre
            if abs(projectile[1] - projectile[2]) < 2 or projectile[1] < 0 or projectile[1] > pyxel.height:
                self.projectiles_liste.remove(projectile)

    def update(self):
        # Mettre à jour la position des bateaux
        for bateau in self.bateaux:
            bateau["x"] += self.vitesse
            if bateau["x"] > pyxel.width:
                bateau["x"] = -bateau["largeur"]

        # Mettre à jour la position du curseur
        self.curseur_x = pyxel.mouse_x
        self.curseur_y = pyxel.mouse_y

        # Vérifier si un ennemi est cliqué et le supprimer
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for ennemi in self.ennemis_liste[:]:
                if (self.curseur_x - ennemi[0]) ** 2 + (self.curseur_y - ennemi[1]) ** 2 < 100:  # Rayon de 10 pixels
                    self.ennemis_liste.remove(ennemi)

        # Tirer un projectile
        self.tirer_projectile()

        # Déplacer les projectiles
        self.deplacer_projectiles()

        # Création des ennemis
        self.ennemis_creation()

        # Mise à jour des positions des ennemis
        self.ennemis_deplacement()

    def draw(self):
        pyxel.cls(0)
        for bateau in self.bateaux:
            pyxel.blt(bateau["x"], bateau["y"], 0, 0, 0, bateau["largeur"], bateau["hauteur"])

        # Dessiner le curseur (petit carré)
        pyxel.rect(self.curseur_x - 2, self.curseur_y - 2, 5, 5, 8)

        # Dessiner les ennemis
        for ennemi in self.ennemis_liste:
            pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

        # Dessiner les projectiles
        for projectile in self.projectiles_liste:
            pyxel.rect(projectile[0], projectile[1], 4, 4, 10)

JeuBateaux()
