import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur_fenetre = 800
hauteur_fenetre = 600
FPS = 60
vitesse_monstre_initiale = 2
vies_tour = 100
vies_joueur = 100
nombre_vagues = 5
nombre_monstres_par_vague = 10

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption('Jeu de Défense de la Tour')

# Chargement des images
image_tour = pygame.image.load('tour.png')
image_joueur = pygame.image.load('joueur.png')
image_monstre = pygame.image.load('monstre.png')

# Fonctions utiles
def afficher_texte(texte, taille, x, y):
    font = pygame.font.Font(None, taille)
    texte_surface = font.render(texte, True, blanc)
    fenetre.blit(texte_surface, (x, y))

def game_over():
    fenetre.fill(rouge)
    afficher_texte("Game Over", 50, largeur_fenetre // 2 - 100, hauteur_fenetre // 2 - 25)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Boucle de jeu principale
def jeu():
    global vies_tour, vies_joueur

    clock = pygame.time.Clock()

    vitesse_monstre = vitesse_monstre_initiale
    vague_actuelle = 1
    victoire = False  # Nouvelle variable pour la condition de victoire

    while vies_tour > 0 and vies_joueur > 0 and not victoire:  # Ajout de la condition de victoire
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestion des événements de déplacement du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            # Déplacement vers le haut (changement de plateforme)
            pass
        elif keys[pygame.K_DOWN]:
            # Déplacement vers le bas (changement de plateforme)
            pass
        elif keys[pygame.K_LEFT]:
            # Déplacement vers la gauche (vers la tour)
            pass
        elif keys[pygame.K_RIGHT]:
            # Déplacement vers la droite (vers le spawn des monstres)
            pass

        # Logique du jeu
        # ...

        # Condition de victoire
        if vague_actuelle > nombre_vagues:
            victoire = True

        # Affichage
        fenetre.fill(blanc)
        fenetre.blit(image_tour, (0, hauteur_fenetre // 2))
        fenetre.blit(image_joueur, (largeur_fenetre // 2, hauteur_fenetre // 2))

        afficher_texte(f"Vies de la tour: {vies_tour}", 20, 10, 10)
        afficher_texte(f"Vies du joueur: {vies_joueur}", 20, largeur_fenetre - 200, 10)

        pygame.display.flip()

        clock.tick(FPS)

    if victoire:
        fenetre.fill(blanc)
        afficher_texte("Victoire !", 50, largeur_fenetre // 2 - 100, hauteur_fenetre // 2 - 25)
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()
    else:
        game_over()

# Démarrage du jeu
if __name__ == "__main__":
    jeu()