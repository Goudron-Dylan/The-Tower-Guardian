import pygame
import sys
import random

#code fonctionnel étape disparition ennemis

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
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
        self.is_moving_right = False
        self.is_moving_left = False
        self.all_sprites_read = False
        self.y_velocity = 0
        self.width = 120  # Largeur du sprite
        self.height = 120  # Hauteur du sprite
        self.health = 8  # Points de vie du joueur

    def move(self):
        if self.is_moving_right:
            self.x += self.speed
        elif self.is_moving_left:
            self.x -= self.speed

    def update_sprite(self):
        if self.is_moving_right:
            if self.current_sprite < len(self.sprites_right) - 3 or self.all_sprites_read:
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites_right)
                if self.current_sprite == 0:
                    self.all_sprites_read = True
            else:
                self.current_sprite = (self.current_sprite + 1) % 3 + (len(self.sprites_right) - 3)
        elif self.is_moving_left:
            if self.current_sprite < len(self.sprites_left) - 3 or self.all_sprites_read:
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites_left)
                if self.current_sprite == 0:
                    self.all_sprites_read = True
            else:
                self.current_sprite = (self.current_sprite + 1) % 3 + (len(self.sprites_left) - 3)

    def draw(self, window):
        if self.is_moving_right:
            window.blit(self.sprites_right[self.current_sprite], (self.x, self.y))
        elif self.is_moving_left:
            window.blit(self.sprites_left[self.current_sprite], (self.x, self.y))
        else:
            window.blit(self.sprites_right[0], (self.x, self.y))

# Classe Monstre
class Monstre:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed  # Les monstres se déplacent vers la gauche
        if self.rect.right < 0:  # Si le monstre est entièrement hors de l'écran à gauche
            self.rect.x = WINDOW_WIDTH  # Réinitialiser sa position à droite de l'écran

    def draw(self, window):
        pygame.draw.rect(window, RED, self.rect)

# Classe Spawner
class Spawner:
    def __init__(self, x, y, width, height, interval, max_monsters_per_wave, total_monsters_limit):
        self.rect = pygame.Rect(x, y, width, height)
        self.interval = interval  # Intervalle en secondes
        self.last_spawn_time = pygame.time.get_ticks()  # Temps depuis le dernier spawn
        self.monsters = []  # Liste pour stocker les monstres
        self.max_monsters_per_wave = max_monsters_per_wave  # Limite d'ennemis par vague
        self.monsters_spawned = 0  # Nombre de monstres générés dans la vague actuelle
        self.wave_count = 0  # Nombre de vagues écoulées
        self.total_monsters_limit = total_monsters_limit  # Limite totale de monstres sur toutes les plateformes
        self.wave_finished_time = 0  # Temps à partir duquel la vague a été terminée
        self.time_between_waves = 6000  # Temps en millisecondes entre les vagues
        self.max_waves = 4  # Nombre maximum de vagues

    def spawn_monster(self):
        current_time = pygame.time.get_ticks()
        if self.wave_count < self.max_waves:
            if current_time - self.last_spawn_time > self.interval * 1000:  # Convertir l'intervalle en millisecondes
                total_monsters = sum(len(spawner.monsters) for spawner in spawners)
                if self.monsters_spawned < self.max_monsters_per_wave and total_monsters < self.total_monsters_limit:
                    # Ajouter un monstre à la liste des monstres
                    self.monsters.append(Monstre(self.rect.x + self.rect.width, self.rect.y, 50, 50, random.randint(1 + self.wave_count, 3 + self.wave_count)))
                    self.last_spawn_time = current_time  # Mettre à jour le temps du dernier spawn
                    self.monsters_spawned += 1  # Incrémenter le compteur de monstres générés
                elif not self.monsters:  # Si tous les monstres ont été vaincus
                    if current_time - self.wave_finished_time > self.time_between_waves:  # Attendre le temps entre les vagues
                        self.wave_count += 1  # Passer à la vague suivante
                        self.monsters_spawned = 0  # Réinitialiser le compteur de monstres générés
                        self.last_spawn_time = current_time  # Réinitialiser le temps du dernier spawn

    def draw(self, window):
        pygame.draw.rect(window, BLUE, self.rect)

    def draw_monsters(self, window):
        for monster in self.monsters:
            monster.draw(window)
            monster.move()
            if monster.rect.right < 0:  # Si le monstre est entièrement hors de l'écran à gauche
                self.monsters.remove(monster)

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

# Création des spawners
spawner1 = Spawner(WINDOW_WIDTH - 100, 890, 50, 50, 2, 15, 15)  # Intervalle en secondes, Limite d'ennemis par vague, Limite totale de monstres sur toutes les plateformes
spawner2 = Spawner(WINDOW_WIDTH - 100, 590, 50, 50, 2, 15, 15)  # Intervalle en secondes, Limite d'ennemis par vague, Limite totale de monstres sur toutes les plateformes
spawner3 = Spawner(WINDOW_WIDTH - 100, 290, 50, 50, 2, 15, 15)  # Intervalle en secondes, Limite d'ennemis par vague, Limite totale de monstres sur toutes les plateformes
spawners = [spawner1, spawner2, spawner3]

# Police de caractères pour l'affichage des points de vie
font = pygame.font.SysFont("Arial", 36)  # Utilisation de la police Arial avec une taille de 36

# Couleur du texte pour les points de vie
text_color = BLACK  # Couleur noire

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.is_moving_right = True
            elif event.key == pygame.K_LEFT:
                player.is_moving_left = True
            elif event.key == pygame.K_UP:
                # Téléportation vers le haut
                for platform in platforms:
                    if player.y > platform.rect.y + platform.rect.height:  # Vérifier si le joueur est au-dessus de la plateforme
                        player.y = platform.rect.y - player.height
                        break
            elif event.key == pygame.K_DOWN:
                # Téléportation vers le bas
                for platform in reversed(platforms):
                    if player.y + player.height < platform.rect.y:  # Vérifier si le joueur peut se tenir debout sur la plateforme
                        player.y = platform.rect.y - player.height
                        break
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.is_moving_right = False
                player.current_sprite = 0
            elif event.key == pygame.K_LEFT:
                player.is_moving_left = False
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

    # Générer des monstres
    for spawner in spawners:
        spawner.spawn_monster()
        spawner.draw(window)
        spawner.draw_monsters(window)

    # Vérifier les collisions entre le joueur et les monstres
    for spawner in spawners:
        for monster in spawner.monsters:
            if player.x < monster.rect.right and player.x + player.width > monster.rect.left and player.y < monster.rect.bottom and player.y + player.height > monster.rect.top:
                # Le joueur a touché un monstre, le monstre est vaincu
                spawner.monsters.remove(monster)
                player.health -= 1  # Le joueur perd un point de vie

    # Affichage des points de vie du joueur
    health_text = font.render(f"Vie : {player.health}", True, text_color)
    window.blit(health_text, (WINDOW_WIDTH - health_text.get_width() - 800, 65))

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le taux de rafraîchissement de l'écran
    pygame.time.Clock().tick(30)

# Quitter pygame
pygame.quit()
sys.exit()