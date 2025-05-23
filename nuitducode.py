import pyxel
import random

class JeuBateaux:
    def __init__(self):
        pyxel.init(256, 256, title="Jeu des Bateaux")

        # Charger les ressources depuis le fichier theme.pyxres
        pyxel.load("theme.pyxres")

        self.bateaux = []
        self.vitesse = 1.5

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

        pyxel.run(self.update, self.draw)

    def ennemis_creation(self):
        """Création aléatoire des ennemis"""
        # Un ennemi par seconde
        if pyxel.frame_count % 30 == 0:
            self.ennemis_liste.append([0, random.randint(220, pyxel.height)])

    def ennemis_deplacement(self):
        """Déplacement des ennemis horizontalement et suppression s'ils sortent du cadre"""
        for ennemi in self.ennemis_liste[:]:
            ennemi[0] += 1
            if ennemi[0] > pyxel.width:
                self.ennemis_liste.remove(ennemi)

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
                if (self.curseur_x - ennemi[0]) ** 2 + (self.curseur_y - ennemi[1]) ** 2 < 16:  # Rayon de 4 pixels
                    self.ennemis_liste.remove(ennemi)

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

JeuBateaux()
