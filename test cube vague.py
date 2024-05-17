import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 700
ENEMY_SIZE = 30
ENEMY_SPEED = 1
SPAWN_POINTS = [(SCREEN_WIDTH - 20, 200), (SCREEN_WIDTH - 20, 350), (SCREEN_WIDTH - 20, 500)]
ENEMIES_COUNT = 15
SPAWN_DELAY = 2  # délai entre deux ennemis, en secondes
WAVE_DELAY = 6  # délai entre deux vagues, en secondes

# Couleurs
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Initialisation de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Test")

clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= ENEMY_SPEED

# Groupes de sprites
enemies = pygame.sprite.Group()

# Fonction de génération d'ennemis
def spawn_enemy():
    spawn_point = random.choice(SPAWN_POINTS)
    enemy = Enemy(*spawn_point)
    enemies.add(enemy)

# Fonction de vérification des collisions avec le bord gauche
def check_border_collision():
    for enemy in enemies:
        if enemy.rect.left <= 0:
            enemy.kill()

# Boucle principale
running = True
wave_timer = 0
enemy_spawned = 0
current_wave_completed = True

while running:
    screen.fill(BLACK)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vérification de la fin de la vague précédente
    if current_wave_completed and len(enemies) == 0 and enemy_spawned >= ENEMIES_COUNT:
        wave_timer += clock.get_rawtime() / 1000
        if wave_timer >= WAVE_DELAY:
            wave_timer = 0
            enemy_spawned = 0
            current_wave_completed = False

    # Génération d'une nouvelle vague si la précédente est terminée
    if not current_wave_completed:
        spawn_timer = clock.get_rawtime() / 1000
        if spawn_timer >= SPAWN_DELAY:
            spawn_timer = 0
            spawn_enemy()
            enemy_spawned += 1
            if enemy_spawned == ENEMIES_COUNT:
                current_wave_completed = True

    # Mise à jour des ennemis
    enemies.update()

    # Vérification des collisions avec le bord gauche
    check_border_collision()

    # Dessin des sprites
    enemies.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
