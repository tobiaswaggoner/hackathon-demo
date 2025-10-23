# Game Objects: Snake, Food, Enemy, Boss, Projectile
import pygame
import random
import math
from config import *

class Snake:
    """The player-controlled snake"""

    def __init__(self):
        # Start in the middle of the grid
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # List of segment positions (each is a [x, y] grid coordinate)
        self.segments = [
            [start_x, start_y],
            [start_x - 1, start_y],
            [start_x - 2, start_y]
        ]

        self.direction = [1, 0]  # Moving right initially
        self.next_direction = [1, 0]  # Buffered input
        self.growth_pending = 0

    def update_direction(self, new_direction):
        """Buffer the next direction (prevents 180° turns)"""
        # Can't reverse direction
        if new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]:
            return
        self.next_direction = new_direction

    def move(self):
        """Move the snake one step"""
        # Apply buffered direction
        self.direction = self.next_direction

        # Calculate new head position
        head = self.segments[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]

        # Add new head
        self.segments.insert(0, head)

        # Remove tail unless growing
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.segments.pop()

    def grow(self, amount=1):
        """Schedule growth for the snake"""
        self.growth_pending += amount

    def check_collision(self):
        """Check for wall collision or self-collision"""
        head = self.segments[0]

        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True

        # Self collision (check if head overlaps any body segment)
        for segment in self.segments[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True

        return False

    def get_head_pos(self):
        """Get head position in pixels"""
        return (self.segments[0][0] * GRID_SIZE + GRID_SIZE // 2,
                self.segments[0][1] * GRID_SIZE + GRID_SIZE // 2)

    def draw(self, surface):
        """Render the snake"""
        # Draw body segments
        for i, segment in enumerate(self.segments):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE

            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, (x, y, GRID_SIZE, GRID_SIZE))

            # Add border for better visibility
            pygame.draw.rect(surface, COLOR_BACKGROUND, (x, y, GRID_SIZE, GRID_SIZE), 1)


class Food:
    """Food items for the snake"""

    def __init__(self, is_bonus=False):
        self.is_bonus = is_bonus
        self.position = self.random_position()
        self.color = COLOR_BONUS_FOOD if is_bonus else COLOR_FOOD
        self.score_value = FOOD_BONUS_SCORE if is_bonus else FOOD_NORMAL_SCORE
        self.growth_value = FOOD_BONUS_GROWTH if is_bonus else FOOD_NORMAL_GROWTH

    def random_position(self):
        """Generate random grid position"""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return [x, y]

    def respawn(self, snake_segments, enemies):
        """Respawn at a new location avoiding snake and enemies"""
        max_attempts = 100
        for _ in range(max_attempts):
            pos = self.random_position()

            # Check if position is free
            if pos not in snake_segments:
                # Check distance from enemies
                too_close = False
                for enemy in enemies:
                    enemy_grid = [enemy.x // GRID_SIZE, enemy.y // GRID_SIZE]
                    if abs(pos[0] - enemy_grid[0]) < 3 and abs(pos[1] - enemy_grid[1]) < 3:
                        too_close = True
                        break

                if not too_close:
                    self.position = pos
                    # Random chance for bonus food
                    self.is_bonus = random.random() < BONUS_FOOD_CHANCE
                    self.color = COLOR_BONUS_FOOD if self.is_bonus else COLOR_FOOD
                    self.score_value = FOOD_BONUS_SCORE if self.is_bonus else FOOD_NORMAL_SCORE
                    self.growth_value = FOOD_BONUS_GROWTH if self.is_bonus else FOOD_NORMAL_GROWTH
                    return

        # Fallback: If all attempts failed, force a position anyway
        self.position = self.random_position()
        self.is_bonus = random.random() < BONUS_FOOD_CHANCE
        self.color = COLOR_BONUS_FOOD if self.is_bonus else COLOR_FOOD
        self.score_value = FOOD_BONUS_SCORE if self.is_bonus else FOOD_NORMAL_SCORE
        self.growth_value = FOOD_BONUS_GROWTH if self.is_bonus else FOOD_NORMAL_GROWTH

    def draw(self, surface):
        """Render the food"""
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE

        # Draw as circle for better visual distinction
        center_x = x + GRID_SIZE // 2
        center_y = y + GRID_SIZE // 2
        radius = GRID_SIZE // 2 - 2

        pygame.draw.circle(surface, self.color, (center_x, center_y), radius)


class Projectile:
    """Projectile shot by enemies or boss"""

    def __init__(self, x, y, angle):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.vx = math.cos(math.radians(angle)) * PROJECTILE_SPEED
        self.vy = math.sin(math.radians(angle)) * PROJECTILE_SPEED
        self.radius = PROJECTILE_RADIUS

    def update(self):
        """Move the projectile"""
        self.x += self.vx
        self.y += self.vy

    def is_off_screen(self):
        """Check if projectile is outside game bounds"""
        return (self.x < 0 or self.x > WINDOW_WIDTH or
                self.y < 0 or self.y > WINDOW_HEIGHT)

    def check_collision(self, snake):
        """Check collision with snake"""
        head_x, head_y = snake.get_head_pos()
        distance = math.sqrt((self.x - head_x)**2 + (self.y - head_y)**2)
        return distance < (self.radius + GRID_SIZE // 2)

    def draw(self, surface):
        """Render the projectile"""
        pygame.draw.circle(surface, COLOR_PROJECTILE, (int(self.x), int(self.y)), self.radius)
        # Add glow effect
        pygame.draw.circle(surface, (255, 100, 100), (int(self.x), int(self.y)), self.radius + 2, 1)


class Enemy:
    """AI-controlled enemy"""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.spawn_x = x
        self.spawn_y = y
        self.health = ENEMY_HEALTH
        self.state = "PATROL"
        self.direction = random.uniform(0, 360)  # Random initial direction
        self.speed = SNAKE_SPEED * ENEMY_SPEED * GRID_SIZE / FPS * 60
        self.patrol_timer = 0
        self.patrol_target_time = random.uniform(2.0, 3.0)  # Fixed patrol duration
        self.shoot_timer = 0
        self.ai_decision_timer = 0

    def update(self, dt, snake, enemies):
        """Update enemy state and position (AI logic will be in ai_behavior.py)"""
        from ai_behavior import update_enemy_ai
        update_enemy_ai(self, dt, snake, enemies)

    def take_damage(self, amount=1):
        """Reduce health and return True if dead"""
        self.health -= amount
        return self.health <= 0

    def draw(self, surface):
        """Render the enemy"""
        # Draw as rectangle
        size = GRID_SIZE * 1.5
        x = int(self.x - size // 2)
        y = int(self.y - size // 2)

        pygame.draw.rect(surface, COLOR_ENEMY, (x, y, size, size))
        pygame.draw.rect(surface, (200, 80, 0), (x, y, size, size), 2)

        # Draw health bar
        health_bar_width = size
        health_bar_height = 4
        health_ratio = self.health / ENEMY_HEALTH

        # Background (red)
        pygame.draw.rect(surface, (100, 0, 0),
                        (x, y - 8, health_bar_width, health_bar_height))
        # Foreground (green)
        pygame.draw.rect(surface, (0, 200, 0),
                        (x, y - 8, health_bar_width * health_ratio, health_bar_height))


class Boss:
    """Powerful boss enemy"""

    def __init__(self):
        # Spawn in center
        self.x = float(WINDOW_WIDTH // 2)
        self.y = float(WINDOW_HEIGHT // 2)
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.speed = SNAKE_SPEED * BOSS_SPEED * GRID_SIZE / FPS * 60
        self.shoot_timer = 0
        self.wave_offset = 0  # For sinusoidal movement

    def update(self, dt, snake):
        """Update boss position and behavior (AI logic will be in ai_behavior.py)"""
        from ai_behavior import update_boss_ai
        update_boss_ai(self, dt, snake)

    def take_damage(self, amount=1):
        """Reduce health and return True if dead"""
        self.health -= amount
        return self.health <= 0

    def draw(self, surface):
        """Render the boss"""
        size = BOSS_SIZE * GRID_SIZE
        x = int(self.x - size // 2)
        y = int(self.y - size // 2)

        # Draw main body
        pygame.draw.rect(surface, COLOR_BOSS, (x, y, size, size))
        # Draw border
        pygame.draw.rect(surface, (200, 0, 0), (x, y, size, size), 3)

        # Draw eyes (intimidating!)
        eye_size = GRID_SIZE // 2
        eye_offset = size // 3
        pygame.draw.circle(surface, (255, 0, 0),
                          (int(self.x - eye_offset), int(self.y - eye_offset)), eye_size)
        pygame.draw.circle(surface, (255, 0, 0),
                          (int(self.x + eye_offset), int(self.y - eye_offset)), eye_size)

        # Draw health bar (large)
        health_bar_width = size
        health_bar_height = 8
        health_ratio = self.health / self.max_health

        # Background
        pygame.draw.rect(surface, (100, 0, 0),
                        (x, y - 15, health_bar_width, health_bar_height))
        # Foreground
        pygame.draw.rect(surface, (0, 255, 0),
                        (x, y - 15, health_bar_width * health_ratio, health_bar_height))
        # Border
        pygame.draw.rect(surface, (255, 255, 255),
                        (x, y - 15, health_bar_width, health_bar_height), 1)
