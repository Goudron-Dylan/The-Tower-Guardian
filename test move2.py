import pygame
import sys

# Initialiser pygame
pygame.init()

# Définir la taille de la fenêtre
WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 1000
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de plateforme")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classe Plateforme
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, BLACK, self.rect)

# Classe Personnage
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
        self.y_velocity = 0
        self.width = 120  # Largeur du sprite
        self.height = 120  # Hauteur du sprite
        self.platform_index = 0  # Indice de la plateforme actuelle

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

    def teleport(self, direction):
        new_platform_index = self.platform_index
        if direction == "up":
            new_platform_index += 1  # Déplace le personnage vers le haut
        elif direction == "down":
            new_platform_index -= 1  # Déplace le personnage vers le bas

        # Vérifie si la nouvelle plateforme existe
        if 0 <= new_platform_index < len(platforms):
            self.platform_index = new_platform_index
            self.y = platforms[self.platform_index].rect.y - self.height

    def draw(self, window):
        if self.right_pressed:
            window.blit(self.sprites_right[self.current_sprite], (self.x, self.y))
        elif self.left_pressed:
            window.blit(self.sprites_left[self.current_sprite], (self.x, self.y))
        else:
            window.blit(self.sprites_right[0], (self.x, self.y))

# Charger les sprites du personnage pour le déplacement vers la droite
player_sprites_right = []
for i in range(1, 16):
    player_sprite = pygame.image.load(f"C:/Users/26269/Documents/pYGAME2/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprite = pygame.transform.scale(player_sprite, (120, 120))  # Adapter la taille du sprite
    player_sprites_right.append(player_sprite)

# Charger les sprites du personnage pour le déplacement vers la gauche
player_sprites_left = []
for i in range(1, 16):
    # Inversion horizontale des images pour le déplacement vers la gauche
    player_sprite = pygame.image.load(f"C:/Users/26269/Documents/pYGAME2/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprite = pygame.transform.scale(player_sprite, (120, 120))  # Adapter la taille du sprite
    player_sprite = pygame.transform.flip(player_sprite, True, False)
    player_sprites_left.append(player_sprite)

# Créer un objet Personnage
player = Personnage(50, WINDOW_HEIGHT // 2, player_sprites_right, player_sprites_left, 5)

# Créer des plateformes
platforms = [
    Platform(0, 950, WINDOW_WIDTH, 20),
    Platform(0, 650, WINDOW_WIDTH, 20),
    Platform(0, 350, WINDOW_WIDTH, 20)
]

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            elif event.key == pygame.K_LEFT:
                player.left_pressed = True
            elif event.key == pygame.K_UP:
                player.teleport("up")
            elif event.key == pygame.K_DOWN:
                player.teleport("down")
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

    # Dessiner les plateformes
    for platform in platforms:
        platform.draw(window)

    # Dessiner le personnage
    player.draw(window)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le taux de rafraîchissement de l'écran
    pygame.time.Clock().tick(30)

# Quitter pygame
pygame.quit()
sys.exit()
