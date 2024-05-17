import sys
import random
import pygame

# Initialiser pygame
pygame.init()

# Définir la taille de la fenêtre
WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 1050
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
    def __init__(self, x, y, sprites_right, sprites_left, attack_sprites_right, attack_sprites_left, speed):
        self.rect = pygame.Rect(x, y, 120, 120)
        self.sprites_right = sprites_right
        self.sprites_left = sprites_left
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        self.speed = speed
        self.current_sprite = 0
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_attacking = False
        self.all_sprites_read = False
        self.y_velocity = 0
        self.health = 8

    def move(self):
        if not self.is_attacking:
            if self.is_moving_right:
                self.rect.x += self.speed
            elif self.is_moving_left:
                self.rect.x -= self.speed

    def update_sprite(self):
        if not self.is_attacking:
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
        if not self.is_attacking:
            if self.is_moving_right:
                window.blit(self.sprites_right[self.current_sprite], self.rect.topleft)
            elif self.is_moving_left:
                window.blit(self.sprites_left[self.current_sprite], self.rect.topleft)
            else:
                window.blit(self.sprites_right[0], self.rect.topleft)
        else:
            if self.is_moving_right:
                window.blit(self.attack_sprites_right[self.current_sprite], self.rect.topleft)
            elif self.is_moving_left:
                window.blit(self.attack_sprites_left[self.current_sprite], self.rect.topleft)

# Classe Monstre
class Monstre:
    def __init__(self, x, y, width, height, speed, color, damage_cooldown):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color
        self.has_hit_player = False
        self.damage_cooldown = damage_cooldown
        self.damage_timer = 0
        self.attack_timer = 0  # Ajouter un attribut pour le timer d'attaque
        self.attack_interval = 2000  # Intervalle entre les attaques (en millisecondes)
        self.damage = 1  # Ajouter un attribut pour les dégâts infligés par le monstre

    def move(self):
        if self.speed != 0:  # Ajoute cette condition pour vérifier si l'ennemi est en mouvement
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.rect.x = WINDOW_WIDTH

    def attack_tower(self, tower):
        # Vérifier la collision avec la tour
        if self.rect.colliderect(tower.rect):
            # Si un ennemi touche la tour, ajuster sa position vers la droite jusqu'à ce qu'il ne soit plus en collision
            while self.rect.colliderect(tower.rect):
                self.rect.x += 1
            
            # Immobiliser l'ennemi en arrêtant son mouvement
            self.speed = 0

            # Gestion des dégâts à la tour
            current_time = pygame.time.get_ticks()
            if current_time - tower.last_damage_time > 2000:
                tower.take_damage(self.damage)  # Infliction de dégâts basés sur l'attribut damage du monstre
                tower.last_damage_time = current_time  # Réinitialisation du timer de dégâts

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

# Class Spawner
class Spawner:
    def __init__(self, x, y, width, height, interval, max_monsters_per_wave, total_monsters_limit):
        self.rect = pygame.Rect(x, y, width, height)
        self.interval = interval
        self.last_spawn_time = pygame.time.get_ticks()
        self.monsters = []
        self.max_monsters_per_wave = max_monsters_per_wave
        self.total_monsters_limit = total_monsters_limit
        self.monsters_spawned = 0
        self.total_monsters_spawned = 0
        self.wave_count = 0
        self.wave_finished_time = 0
        self.time_between_waves = 6000
        self.max_waves = 4
        self.color = RED
        self.wave_number = 0

    def spawn_monster(self):
        current_time = pygame.time.get_ticks()
        if self.wave_count < self.max_waves:
            if current_time - self.last_spawn_time > self.interval * 1000:
                if self.monsters_spawned < self.max_monsters_per_wave and self.total_monsters_spawned < self.total_monsters_limit:
                    random_platform = random.choice(platforms)
                    self.monsters.append(Monstre(random_platform.rect.x + random_platform.rect.width, random_platform.rect.y - 50, 50, 50, random.randint(1 + self.wave_count, 3 + self.wave_count), self.color, 60))
                    self.monsters[-1].damage = 1 + self.wave_count  # Ajouter cette ligne pour attribuer des dégâts en fonction de la vague
                    self.last_spawn_time = current_time
                    self.monsters_spawned += 1
                    self.total_monsters_spawned += 1
                elif not self.monsters:
                    if current_time - self.wave_finished_time > self.time_between_waves:
                        self.wave_count += 1
                        self.monsters_spawned = 0
                        self.last_spawn_time = current_time
                        self.wave_finished_time = 0
                        self.total_monsters_spawned = 0
                        self.color = BLUE if self.wave_count % 2 == 0 else RED
                        self.wave_number += 1

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def draw_monsters(self, window):
        for monster in self.monsters:
            monster.draw(window)
            monster.move()
            if monster.rect.right < 0:
                self.monsters.remove(monster)

    def draw_wave_number(self, window):
        font = pygame.font.SysFont("Arial", 72)
        text = font.render(f"Vague {self.wave_number}", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(text, text_rect)

# Classe Boule de feu
class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = 10
        self.direction = direction

    def move(self):
        self.x += self.speed * self.direction

    def draw(self, window):
        pygame.draw.circle(window, (0, 255, 0), (self.x, self.y), self.radius)

# Charger les sprites du personnage pour le déplacement vers la droite
player_sprites_right = []
for i in range(1, 16):
    player_sprite = pygame.image.load(f"D:/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprite = pygame.transform.scale(player_sprite, (120, 120))
    player_sprites_right.append(player_sprite)

# Charger les sprites du personnage pour le déplacement vers la gauche
player_sprites_left = []
for i in range(1, 16):
    player_sprite = pygame.image.load(f"D:/Pygame/The Tower Guardian/emmerde/NewPiskel{i}.png")
    player_sprite = pygame.transform.scale(player_sprite, (120, 120))
    player_sprite = pygame.transform.flip(player_sprite, True, False)
    player_sprites_left.append(player_sprite)

# Charger les sprites du personnage pour l'attaque vers la droite
attack_sprites_right = []
for i in range(1, 11):
    attack_sprite = pygame.image.load(f"D:/Pygame/The Tower Guardian/Boule de feu/attack_right{i}.png")
    attack_sprite = pygame.transform.scale(attack_sprite, (120, 120))
    attack_sprites_right.append(attack_sprite)

# Charger les sprites du personnage pour l'attaque vers la gauche
attack_sprites_left = []
for i in range(1, 11):
    attack_sprite = pygame.image.load(f"D:/Pygame/The Tower Guardian/Boule de feu/attack_right{i}.png")
    attack_sprite = pygame.transform.scale(attack_sprite, (120, 120))
    attack_sprite = pygame.transform.flip(attack_sprite, True, False)
    attack_sprites_left.append(attack_sprite)

# Créer un objet Personnage
player = Personnage(900, WINDOW_HEIGHT // 2, player_sprites_right, player_sprites_left, attack_sprites_right, attack_sprites_left, 5)

# Créer des plateformes
platforms = [
    Platform(0, 950, WINDOW_WIDTH, 20),
    Platform(0, 650, WINDOW_WIDTH, 20),
    Platform(0, 350, WINDOW_WIDTH, 20)
]

# Création du spawner
spawner = Spawner(WINDOW_WIDTH - 100, 890, 50, 50, 2, 15, 15)

# Liste pour stocker les boules de feu
fireballs = []

# Police de caractères pour l'affichage des points de vie
font = pygame.font.SysFont("Arial", 36)
text_color = BLACK

# Classe Tour
class Tour:
    def __init__(self, x, y, width, height, health):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.max_health = health
        self.last_damage_time = pygame.time.get_ticks()  # Ajoutez cette ligne pour initialiser le timer de dégâts

    def draw(self, window):
        # Dessiner le corps de la tour
        pygame.draw.rect(window, (0, 255, 0), self.rect)  # Vert pour le corps de la tour

        # Dessiner la barre de vie
        health_bar_width = self.rect.width * (self.health / self.max_health)
        if self.health > 0.6 * self.max_health:
            remaining_color = (0, 255, 0)  # Vert pour la partie restante
            lost_color = (255, 0, 0)  # Rouge pour la partie perdue
        elif self.health > 0.3 * self.max_health:
            remaining_color = (255, 255, 0)  # Jaune pour la partie restante
            lost_color = (255, 0, 0)  # Rouge pour la partie perdue
        else:
            remaining_color = (255, 0, 0)  # Rouge pour la partie restante
            lost_color = (255, 0, 0)  # Rouge pour la partie perdue

        # Dessiner la partie de la barre de vie restante
        pygame.draw.rect(window, remaining_color, (self.rect.x, self.rect.y - 20, health_bar_width, 10))

        # Dessiner la partie de la barre de vie perdue
        lost_health_bar_width = self.rect.width - health_bar_width
        lost_health_bar_rect = pygame.Rect(self.rect.x + health_bar_width, self.rect.y - 20, lost_health_bar_width, 10)
        pygame.draw.rect(window, (255, 0, 0), lost_health_bar_rect)  # Rouge pour la partie perdue

        # Dessiner le contour de la barre de vie
        pygame.draw.rect(window, (0, 0, 0), (self.rect.x, self.rect.y - 20, self.rect.width, 10), 2)

    def take_damage(self, damage):
        self.health -= damage
        print(f"Tour - Santé actuelle : {self.health}/{self.max_health}")  # Ajoutez cette ligne pour afficher la santé actuelle de la tour

    def draw_health_bar(self, window):
        tour_health_bar_width = 400
        tour_health_bar_height = 30
        tour_health_bar_x = 600
        tour_health_bar_y = 100

        # Calculer la largeur de la barre de vie restante en fonction de la santé actuelle de la tour
        health_bar_width = tour_health_bar_width * (self.health / self.max_health)

        # Dessiner la partie de la barre de vie restante
        pygame.draw.rect(window, (0, 255, 0), (tour_health_bar_x, tour_health_bar_y, health_bar_width, tour_health_bar_height))

        # Dessiner la partie de la barre de vie perdue
        lost_health_bar_width = tour_health_bar_width - health_bar_width
        pygame.draw.rect(window, (255, 0, 0), (tour_health_bar_x + health_bar_width, tour_health_bar_y, lost_health_bar_width, tour_health_bar_height))

        # Dessiner le contour de la barre de vie
        pygame.draw.rect(window, (0, 0, 0), (tour_health_bar_x, tour_health_bar_y, tour_health_bar_width, tour_health_bar_height), 2)



# Créer une tour à gauche de l'écran
tour = Tour(0, 0, 300, WINDOW_HEIGHT, 40)

# Boucle principale du jeu
running = True
last_damage_time = pygame.time.get_ticks()  # Ajouter cette ligne pour initialiser le timer de dégâts
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
                    if player.rect.y > platform.rect.y + platform.rect.height:  # Vérifier si le joueur est au-dessus de la plateforme
                        player.rect.y = platform.rect.y - player.rect.height
                        break
            elif event.key == pygame.K_DOWN:
                # Téléportation vers le bas
                for platform in reversed(platforms):
                    if player.rect.y + player.rect.height < platform.rect.y:  # Vérifier si le joueur peut se tenir debout sur la plateforme
                        player.rect.y = platform.rect.y - player.rect.height
                        break
            elif event.key == pygame.K_e and (player.is_moving_left or player.is_moving_right):
                # Lancer l'attaque si le joueur se déplace
                player.is_attacking = True
                player.current_sprite = 0
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

    # Gestion de l'attaque du personnage
    if player.is_attacking:
        player.current_sprite += 1
        if player.current_sprite >= len(player.attack_sprites_right):
            player.current_sprite = 0
            player.is_attacking = False
            # Lancer la boule de feu
            if player.is_moving_right:
                fireball = Fireball(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2, 1)
            elif player.is_moving_left:
                fireball = Fireball(player.rect.x - 0.1 * player.rect.width, player.rect.y + player.rect.height // 2, -1)
            fireballs.append(fireball)

    # Gestion des boules de feu
    fireballs_to_remove = []  # Liste temporaire pour stocker les boules de feu à supprimer
    for fireball in fireballs:
        fireball.move()
        # Vérifier si la boule de feu touche un monstre
        for monster in spawner.monsters:
            if fireball.x + fireball.radius > monster.rect.left and fireball.x - fireball.radius < monster.rect.right and fireball.y + fireball.radius > monster.rect.top and fireball.y - fireball.radius < monster.rect.bottom:
                # La boule de feu a touché un monstre, marquer la boule de feu et le monstre pour suppression
                fireballs_to_remove.append(fireball)
                spawner.monsters.remove(monster)
                break
        # Vérifier si la boule de feu a atteint sa limite de distance
        if fireball.x > player.rect.x + 400 or fireball.x < player.rect.x - 400:
            fireballs_to_remove.append(fireball)

    # Supprimer les boules de feu marquées de la liste principale
    for fireball in fireballs_to_remove:
        fireballs.remove(fireball)

    # Effacer l'écran
    window.fill(WHITE)

    # Affichage du numéro de la vague
    spawner.draw_wave_number(window)

    # Dessiner la tour
    tour.draw(window)
    tour.draw_health_bar(window)  # Ajouter cette ligne pour dessiner la barre de vie de la tour

    # Vérifier la collision entre le joueur et la tour
    if player.rect.colliderect(tour.rect):
        # Si le joueur touche la tour, ajuster sa position pour l'empêcher de traverser la tour
        if player.is_moving_right:
            player.rect.x = tour.rect.left - player.rect.width
        elif player.is_moving_left:
            player.rect.x = tour.rect.right

    # Dessiner les plateformes
    for platform in platforms:
        platform.draw(window)

    # Dessiner le personnage
    player.draw(window)

    # Générer des monstres
    spawner.spawn_monster()  # Appel de la méthode spawn_monster()
    spawner.draw(window)
    spawner.draw_monsters(window)

    # Dessiner et déplacer les boules de feu
    for fireball in fireballs:
        fireball.draw(window)

    # Vérifier les collisions entre le joueur et les monstres
    for monster in spawner.monsters:
        if not monster.has_hit_player and player.rect.x < monster.rect.right and player.rect.x + player.rect.width > monster.rect.left and player.rect.y < monster.rect.bottom and player.rect.y + player.rect.height > monster.rect.top:
            # Le joueur a touché un monstre pour la première fois
            monster.has_hit_player = True
            player.health -= 1  # Le joueur perd un point de vie
        elif monster.has_hit_player and (player.rect.x >= monster.rect.right or player.rect.x + player.rect.width <= monster.rect.left or player.rect.y >= monster.rect.bottom or player.rect.y + player.rect.height <= monster.rect.top):
            # Réinitialiser l'état de collision si le joueur n'est plus en collision avec le monstre
            monster.has_hit_player = False

    # Vérifier les collisions entre les ennemis et la tour
    for monster in spawner.monsters:
        monster.attack_tower(tour)
        if monster.rect.colliderect(tour.rect):
            # Si un ennemi touche la tour, ajuster sa position vers la droite jusqu'à ce qu'il ne soit plus en collision
            while monster.rect.colliderect(tour.rect):
                monster.rect.x += 1
            
            # Immobiliser l'ennemi en arrêtant son mouvement
            monster.speed = 0

            # Gestion des dégâts à la tour toutes les 2 secondes si l'ennemi est immobile
            current_time = pygame.time.get_ticks()
            if current_time - last_damage_time > 2000:
                tour.take_damage(1)  # Infliction de dégâts
                last_damage_time = current_time  # Réinitialisation du timer de dégâts

    # Affichage des points de vie du joueur
    health_text = font.render(f"Vie : {player.health}", True, text_color)
    window.blit(health_text, (WINDOW_WIDTH - health_text.get_width() - 600, 100))

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter le taux de rafraîchissement de l'écran
    pygame.time.Clock().tick(30)

# Quitter pygame
pygame.quit()
sys.exit()