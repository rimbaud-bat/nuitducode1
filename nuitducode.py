import pyxel
import random

class SpaceGame:
    def __init__(self):
        pyxel.init(256, 256, title="Nuit du code")

        # Initialisation du vaisseau
        self.ship_x = 75
        self.ship_y = 100exit

        # Initialisation des astéroïdes
        self.asteroids = []
        self.score = 0

        # Charger les ressources
        pyxel.load("assets.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self):
        # Déplacement du vaisseau
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ship_x = max(self.ship_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ship_x = min(self.ship_x + 2, pyxel.width - 8)

        # Génération d'astéroïdes
        if pyxel.frame_count % 30 == 0:
            self.asteroids.append([random.randint(0, pyxel.width - 8), -8])

        # Mise à jour des positions des astéroïdes
        for asteroid in self.asteroids:
            asteroid[1] += 2

        # Suppression des astéroïdes hors écran
        self.asteroids = [asteroid for asteroid in self.asteroids if asteroid[1] < pyxel.height]

        # Détection des collisions
        for asteroid in self.asteroids:
            if (self.ship_x < asteroid[0] + 8 and
                self.ship_x + 8 > asteroid[0] and
                self.ship_y < asteroid[1] + 8 and
                self.ship_y + 8 > asteroid[1]):
                pyxel.quit()

        # Augmentation du score
        self.score += 1

    def draw(self):
        # Effacer l'écran
        pyxel.cls(0)

        # Dessiner le vaisseau
        pyxel.blt(self.ship_x, self.ship_y, 0, 0, 0, 8, 8)

        # Dessiner les astéroïdes
        for asteroid in self.asteroids:
            pyxel.blt(asteroid[0], asteroid[1], 0, 8, 0, 8, 8)

        # Afficher le score
        pyxel.text(5, 5, f"Score: {self.score}", 7)

SpaceGame()
