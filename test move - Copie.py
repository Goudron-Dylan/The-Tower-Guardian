import pygame
import sys

class Plateforme:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Personnage:
    def __init__(self, x, y, sprites_right, sprites_left, speed):
        self.x = x
        self.y = y
        self.width = 120  # Largeur du sprite
        self.height = 120  # Hauteur du sprite
        self.sprites_right = sprites_right
        self.sprites_left = sprites_left
        self.speed = speed
        self.current_sprite = 0
        self.right_pressed = False
        self.left_pressed = False
        self.up_pressed = False
        self.on_ground = False

    def move(self, platforms):
        # Déplacement horizontal
        if self.right_pressed:
            self.x += self.speed
        elif self.left_pressed:
            self.x -= self.speed

        # Déplacement vertical (saute si sur le sol)
        if self.up_pressed and self.on_ground:
            self.y -= 10
            self.on_ground = False

        # Appliquer la gravité
        self.y += 0.01

        # Vérifier les collisions avec les plateformes
        self.check_platform_collisions(platforms)

    def check_platform_collisions(self, platforms):
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Si le personnage est au-dessus de la plateforme, il est sur le sol
                if self.y + self.height < platform.rect.centery:
                    self.on_ground = True
                # Si le personnage est en dessous de la plateforme, ajustez sa position verticalement
                elif self.y < platform.rect.bottom:
                    self.y = platform.rect.bottom
                # Si le personnage est au-dessus de la plateforme, ajustez sa position verticalement
                elif self.y > platform.rect.y + platform.rect.height - self.height:
                    self.y = platform.rect.y + platform.rect.height - self.height


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
    player_sprite = pygame.image.load(f"D:/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprites_right.append(player_sprite)

# Charger les sprites du personnage pour le déplacement vers la gauche
player_sprites_left = []
for i in range(1, 16):
    player_sprite = pygame.transform.flip(pygame.image.load(f"D:/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png"), True, False)
    player_sprites_left.append(player_sprite)

# Obtenir la hauteur du sprite du personnage (après avoir chargé les sprites)
player_sprite = player_sprites_right[0]  # Utilisez le premier sprite pour obtenir la hauteur
player_height = player_sprite.get_rect().height

# Créer une plateforme en bas de la fenêtre
bottom_platform = Plateforme(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 20)


# Créer un objet Personnage et positionner sur la plateforme
player = Personnage(50, WINDOW_HEIGHT - 22 - bottom_platform.rect.height - player_height, player_sprites_right, player_sprites_left, 5)

print("Position du personnage:", player.x, player.y)
print("Position de la plateforme:", bottom_platform.rect.x, bottom_platform.rect.y)

# Liste des plateformes
platforms = [bottom_platform]

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
                player.up_pressed = True
            elif event.key == pygame.K_DOWN:
                player.down_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            elif event.key == pygame.K_LEFT:
                player.left_pressed = False
            elif event.key == pygame.K_UP:
                player.up_pressed = False
            elif event.key == pygame.K_DOWN:
                player.down_pressed = False

    # Gestion du mouvement et de l'animation du personnage
    player.move(platforms)

    # Effacer l'écran
    window.fill(WHITE)

    # Dessiner le personnage
    player.draw(window)

    # Dessiner les plateformes
    for platform in platforms:
        pygame.draw.rect(window, (0, 0, 0), platform.rect)

    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter pygame
pygame.quit()
sys.exit()
