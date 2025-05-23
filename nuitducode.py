import pyxel

class JeuBateaux:
    def __init__(self):
        pyxel.init(160, 120, title="Jeu des Bateaux")

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

        pyxel.run(self.update, self.draw)

    def update(self):
        # Mettre à jour la position des bateaux
        for bateau in self.bateaux:
            bateau["x"] += self.vitesse

            # Réinitialiser la position si le bateau sort de l'écran
            if bateau["x"] > pyxel.width:
                bateau["x"] = -bateau["largeur"]

    def draw(self):
        # Effacer l'écran
        pyxel.cls(0)

        # Dessiner les bateaux
        for bateau in self.bateaux:
            pyxel.blt(bateau["x"], bateau["y"], 0, 0, 0, bateau["largeur"], bateau["hauteur"])

JeuBateaux()
