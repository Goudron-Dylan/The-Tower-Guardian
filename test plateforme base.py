import pygame
import sys
# class barre de vie
# class Monstres
class Personnage:
    def __init__(self, x, y, sprites_right, sprites_left, speed):
        self.x = x
        self.y = y
        self.sprites_right = sprites_right
        self.sprites_left = sprites_left
        self.speed = speed
        self.current_sprite = 0
        self.right_pressed = False
        self.left_pressed = False
        self.all_sprites_read = False

    def move(self):
        if self.right_pressed:
            self.x += self.speed
        elif self.left_pressed:
            self.x -= self.speed

    def update_sprite(self):
        if self.right_pressed:
            if self.current_sprite < len(self.sprites_right) - 3 or self.all_sprites_read:
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites_right)
                if self.current_sprite == 0:
                    self.all_sprites_read = True
            else:
                self.current_sprite = (self.current_sprite + 1) % 3 + (len(self.sprites_right) - 3)
        elif self.left_pressed:
            if self.current_sprite < len(self.sprites_left) - 3 or self.all_sprites_read:
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites_left)
                if self.current_sprite == 0:
                    self.all_sprites_read = True
            else:
                self.current_sprite = (self.current_sprite + 1) % 3 + (len(self.sprites_left) - 3)

    def draw(self, window):
        if self.right_pressed:
            window.blit(self.sprites_right[self.current_sprite], (self.x, self.y))
        elif self.left_pressed:
            window.blit(self.sprites_left[self.current_sprite], (self.x, self.y))
        else:
            window.blit(self.sprites_right[0], (self.x, self.y))


# Initialiser pygame
pygame.init()

# Définir la taille de la fenêtre
WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 1000
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Déplacement du personnage avec plusieurs sprites")

# Couleur de fond
WHITE = (255, 255, 255)

# Charger les sprites du personnage pour le déplacement vers la droite
player_sprites_right = []
for i in range(1, 16):
    player_sprite = pygame.image.load(f"C:/Users/26269/Documents/pYGAME2/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprites_right.append(player_sprite)

# Charger les sprites du personnage pour le déplacement vers la gauche
player_sprites_left = []
for i in range(1, 16):
    # Inversion horizontale des images pour le déplacement vers la gauche
    player_sprite = pygame.transform.flip(pygame.image.load(f"C:/Users/26269/Documents/pYGAME2/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png"), True, False)
    player_sprites_left.append(player_sprite)

# Créer un objet Personnage
player = Personnage(50, WINDOW_HEIGHT // 2, player_sprites_right, player_sprites_left, 5)

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            elif event.key == pygame.K_LEFT:
                player.left_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
                player.current_sprite = 0
            elif event.key == pygame.K_LEFT:
                player.left_pressed = False
                player.current_sprite = 0

    # Gestion du mouvement et de l'animation du personnage
    player.move()
    player.update_sprite()

    # Effacer l'écran
    window.fill(WHITE)

    # Dessiner le personnage
    player.draw(window)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le taux de rafraîchissement de l'écran
    pygame.time.Clock().tick(30)

# Quitter pygame
pygame.quit()
sys.exit()
