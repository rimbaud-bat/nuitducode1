import pyxel

class JeuBateaux:
    def __init__(self):
        pyxel.init(120, 120, title="Jeu des Bateaux")

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

        # Liste des positions enregistrées lors des clics
        self.positions_clic = []

        pyxel.run(self.update, self.draw)

    def update(self):
        # Mettre à jour la position des bateaux
        for bateau in self.bateaux:
            bateau["x"] += self.vitesse
            if bateau["x"] > pyxel.width:
                bateau["x"] = -bateau["largeur"]

        # Mettre à jour la position du curseur
        self.curseur_x = pyxel.mouse_x
        self.curseur_y = pyxel.mouse_y

        # Enregistrer la position lors d'un clic gauche
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.positions_clic.append((self.curseur_x, self.curseur_y))

    def draw(self):
        pyxel.cls(0)
        for bateau in self.bateaux:
            pyxel.blt(bateau["x"], bateau["y"], 0, 0, 0, bateau["largeur"], bateau["hauteur"])

        # Dessiner le curseur (petit carré)
        pyxel.rect(self.curseur_x - 2, self.curseur_y - 2, 5, 5, 8)

        # Dessiner les positions enregistrées (petits cercles)
        for pos in self.positions_clic:
            pyxel.circ(pos[0], pos[1], 2, 10)

JeuBateaux()
