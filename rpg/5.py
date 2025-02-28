import pygame
import sys
import os
import math
import time
import random
from enum import Enum, auto

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

class PlayerClass(Enum):
    WARRIOR = auto()
    MAGE = auto()
    ARCHER = auto()
    ROGUE = auto()

class Weather(Enum):
    CLEAR = auto()
    RAIN = auto()
    STORM = auto()
    FOG = auto()

class TimeOfDay(Enum):
    DAWN = auto()
    DAY = auto()
    DUSK = auto()
    NIGHT = auto()
class QuestStatus(Enum):
    INACTIVE = auto()
    ACTIVE = auto()
    COMPLETED = auto()

class Quest:
    def __init__(self, description, target_score):
        self.description = description
        self.target_score = target_score
        self.status = QuestStatus.INACTIVE
    
    def check_completion(self, score):
        if self.status == QuestStatus.ACTIVE and score >= self.target_score:
            self.status = QuestStatus.COMPLETED
            return True
        return False

# Quest system
available_quests = [
    Quest("Reach 50 points", 50),
    Quest("Reach 100 points", 100),
    Quest("Reach 200 points", 200)
]
current_quest_index = 0

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simple RPG")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Enhanced stats
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.base_speed = 5
        self.speed = self.base_speed
        self.attack_power = 10
        self.defense = 5
        self.level = 1
        self.experience = 0
        
        # Movement state
        self.sprinting = False
        self.direction = Direction.SOUTH
        self.last_attack = 0
        self.attack_cooldown = 500  # milliseconds

    def move(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        
        # Sprint mechanic
        self.sprinting = keys[pygame.K_LSHIFT] and self.stamina > 0
        self.speed = self.base_speed * (1.5 if self.sprinting else 1)
        
        # Diagonal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.direction = Direction.WEST
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.direction = Direction.EAST
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
            self.direction = Direction.NORTH
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
            self.direction = Direction.SOUTH
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/√2
            dy *= 0.707
            
        # Update position with boundary checking
        new_x = max(0, min(WINDOW_WIDTH - self.rect.width, self.rect.x + dx))
        new_y = max(0, min(WINDOW_HEIGHT - self.rect.height, self.rect.y + dy))
        self.rect.x = new_x
        self.rect.y = new_y
        
        # Update stamina
        if self.sprinting:
            self.stamina = max(0, self.stamina - 1)
        else:
            self.stamina = min(self.max_stamina, self.stamina + 0.5)
            
    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            self.last_attack = current_time
            return True
        return False

    def level_up(self):
        if self.experience >= 100:
            self.level += 1
            self.experience -= 100
            self.max_health += 20
            self.health = self.max_health
            self.attack_power += 5
            self.defense += 2
            return True
        return False

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Enhanced stats
        self.health = 50
        self.max_health = 50
        self.speed = random.uniform(1.5, 3.0)
        self.damage = 10
        self.behavior_type = random.choice(['chase', 'circle', 'ambush'])
        self.attack_range = 100
        self.circle_radius = 150
        self.circle_angle = random.uniform(0, 2 * math.pi)
        self.last_attack = 0
        self.attack_cooldown = 1000
        
    def move_towards_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if self.behavior_type == 'chase':
            if distance > 0:
                dx = (dx / distance) * self.speed
                dy = (dy / distance) * self.speed
                self.rect.x += dx
                self.rect.y += dy
                
        elif self.behavior_type == 'circle':
            self.circle_angle += 0.02
            self.rect.x = player.rect.x + math.cos(self.circle_angle) * self.circle_radius
            self.rect.y = player.rect.y + math.sin(self.circle_angle) * self.circle_radius
            
        elif self.behavior_type == 'ambush':
            if distance > self.attack_range:
                # Stay still when far
                pass
            else:
                # Charge at player when in range
                dx = (dx / distance) * self.speed * 2
                dy = (dy / distance) * self.speed * 2
                self.rect.x += dx
                self.rect.y += dy
        
        # Keep enemy within screen bounds
        self.rect.x = max(0, min(WINDOW_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(WINDOW_HEIGHT - self.rect.height, self.rect.y))
        
    def attack_player(self, player, current_time):
        distance = math.sqrt((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        if distance < self.attack_range and current_time - self.last_attack >= self.attack_cooldown:
            player.health -= self.damage
            self.last_attack = current_time
            return True
        return False
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
healing_items = pygame.sprite.Group()

# Create player
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
all_sprites.add(player)

# Create initial enemies
for _ in range(5):
    enemy = Enemy(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game state initialization
running = True
game_over = False
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)
current_state = GameState.PLAYING

# Main game loop
while running and current_state != GameState.GAME_OVER:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if player.attack():
                # Check for enemies in range
                for enemy in enemies:
                    dx = enemy.rect.x - player.rect.x
                    dy = enemy.rect.y - player.rect.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < 50:  # Attack range
                        if enemy.take_damage(player.attack_power):
                            score += 20
            
    if not game_over:
        # Update game state
        player.move()
        for enemy in enemies:
            enemy.move_towards_player(player)
        
        # Add after enemy and player updates
        all_sprites.update()
            
        # Spawn healing items
        if random.random() < 0.02:
            healing = pygame.sprite.Sprite()
            healing.image = pygame.Surface([15, 15])
            healing.image.fill(GREEN)
            healing.rect = healing.image.get_rect()
            healing.rect.x = random.randint(0, WINDOW_WIDTH)
            healing.rect.y = random.randint(0, WINDOW_HEIGHT)
            healing_items.add(healing)
            all_sprites.add(healing)

        # Check collisions
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player.health -= 1
            # Screen shake effect
            original_pos = screen.get_rect().copy()
            for _ in range(5):  # Duration of shake
                offset = [random.randint(-5, 5), random.randint(-5, 5)]
                screen.blit(screen, offset)
                pygame.display.flip()
                pygame.time.delay(50)
            screen.blit(screen, original_pos)
            
            if player.health <= 0:
                current_state = GameState.GAME_OVER

        # Check for healing item collisions
        healing_hits = pygame.sprite.spritecollide(player, healing_items, True)
        if healing_hits:
            player.health = min(100, player.health + 20)
            score += 10
            # Play heal sound if available
            # pygame.mixer.Sound('heal.wav').play()

        # Draw game state
        screen.fill(WHITE)
        all_sprites.draw(screen)
        
        # Draw UI
        pygame.draw.rect(screen, RED, (10, 10, 100, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, player.health, 20))
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 40))
        
        # Add to the UI drawing section
        if not game_over:
            # ...existing UI code...
            
            # Draw current quest status
            if current_quest_index < len(available_quests):
                current_quest = available_quests[current_quest_index]
                quest_text = f"Current Quest: {current_quest.description}"
                quest_status = font.render(quest_text, True, BLACK)
                screen.blit(quest_status, (10, 70))
        
    else:
        # Game Over screen
        screen.fill(WHITE)  # Clear screen first
        font_large = pygame.font.Font(None, 74)
        text = font_large.render(f'Game Over - Score: {score}', True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()