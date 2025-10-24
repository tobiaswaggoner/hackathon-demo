# Enemy AI for Snake Cool Game
import pygame
import random
import math
from constants import *

class Enemy:
    def __init__(self, position):
        """Initialize enemy at position"""
        self.position = list(position)  # [x, y] in grid coordinates
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.last_direction_change = 0
        self.animation_offset = random.random() * 10

        # AI state
        self.mode = 'wander'  # 'wander' or 'chase'

    def get_distance_to(self, target_pos):
        """Calculate Manhattan distance to target"""
        return abs(self.position[0] - target_pos[0]) + abs(self.position[1] - target_pos[1])

    def calculate_smart_direction(self, target_pos, obstacles):
        """Calculate intelligent direction towards target avoiding obstacles"""
        current_x, current_y = self.position
        target_x, target_y = target_pos

        # Possible moves with priorities
        moves = []

        # Calculate desirability for each direction
        directions = [UP, DOWN, LEFT, RIGHT]
        for direction in directions:
            new_x = current_x + direction[0]
            new_y = current_y + direction[1]

            # Skip if out of bounds
            if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                continue

            # Skip if obstacle
            if (new_x, new_y) in obstacles:
                continue

            # Calculate distance to target from this position
            distance = abs(new_x - target_x) + abs(new_y - target_y)

            # Add some randomness to make it less predictable
            distance += random.random() * 2

            moves.append((distance, direction))

        # Choose the direction that minimizes distance
        if moves:
            moves.sort(key=lambda x: x[0])
            return moves[0][1]

        # If no valid moves, return current direction
        return self.direction

    def wander(self):
        """Random wandering behavior"""
        if random.random() < 0.1:  # 10% chance to change direction
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def update(self, snake_head_pos, snake_body, current_time):
        """Update enemy AI and position"""
        # Determine mode based on distance to snake
        distance = self.get_distance_to(snake_head_pos)

        if distance < ENEMY_ACTIVATION_RADIUS:
            self.mode = 'chase'
        else:
            self.mode = 'wander'

        # Direction change cooldown
        if current_time - self.last_direction_change > ENEMY_DIRECTION_COOLDOWN:
            if self.mode == 'chase':
                # Chase the snake, avoiding body
                self.direction = self.calculate_smart_direction(snake_head_pos, set(snake_body))
            else:
                # Wander randomly
                self.wander()

            self.last_direction_change = current_time

        # Move in current direction
        new_x = self.position[0] + self.direction[0]
        new_y = self.position[1] + self.direction[1]

        # Check bounds
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            # Don't move into snake body
            if (new_x, new_y) not in snake_body:
                self.position = [new_x, new_y]
            else:
                # Hit obstacle, change direction
                self.wander()

        # Update animation
        self.animation_offset += 0.05

    def get_position(self):
        """Get current position as tuple"""
        return tuple(self.position)

    def draw(self, surface):
        """Draw enemy with effects"""
        x, y = self.position
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE

        # Pulsing glow effect
        pulse = math.sin(self.animation_offset) * 0.3 + 0.7
        glow_color = tuple(int(c * pulse) for c in ENEMY_GLOW_COLOR)

        # Glow layers
        for i in range(2):
            glow_size = CELL_SIZE + 6 - i * 2
            glow_offset = (CELL_SIZE - glow_size) // 2
            glow_rect = pygame.Rect(
                pixel_x + glow_offset,
                pixel_y + glow_offset,
                glow_size, glow_size
            )
            pygame.draw.rect(surface, glow_color, glow_rect, 2 - i, border_radius=6)

        # Main enemy body
        enemy_rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, ENEMY_COLOR, enemy_rect, border_radius=6)

        # Eye effect based on mode
        if self.mode == 'chase':
            # Angry eyes when chasing
            eye_color = (255, 255, 0)
        else:
            # Normal eyes when wandering
            eye_color = (255, 200, 200)

        eye_size = 4
        left_eye = (pixel_x + CELL_SIZE // 3, pixel_y + CELL_SIZE // 3)
        right_eye = (pixel_x + 2 * CELL_SIZE // 3, pixel_y + CELL_SIZE // 3)
        pygame.draw.circle(surface, eye_color, left_eye, eye_size)
        pygame.draw.circle(surface, eye_color, right_eye, eye_size)


class EnemyManager:
    def __init__(self):
        """Manage all enemies"""
        self.enemies = []

    def spawn_enemy(self, snake_body, food_pos, existing_positions):
        """Spawn new enemy at safe location"""
        attempts = 0
        max_attempts = 50

        occupied = set(snake_body)
        occupied.add(food_pos)
        occupied.update(existing_positions)

        while attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            # Must be far from snake head
            snake_head = snake_body[0]
            distance = abs(x - snake_head[0]) + abs(y - snake_head[1])

            if (x, y) not in occupied and distance > 10:
                enemy = Enemy((x, y))
                self.enemies.append(enemy)
                return True

            attempts += 1

        return False

    def update(self, snake_head_pos, snake_body, current_time):
        """Update all enemies"""
        for enemy in self.enemies:
            enemy.update(snake_head_pos, snake_body, current_time)

    def draw(self, surface):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(surface)

    def check_collision_with_snake(self, snake_head_pos):
        """Check if any enemy hit the snake"""
        for enemy in self.enemies:
            if enemy.get_position() == snake_head_pos:
                return True
        return False

    def get_positions(self):
        """Get all enemy positions"""
        return [enemy.get_position() for enemy in self.enemies]

    def clear(self):
        """Remove all enemies"""
        self.enemies.clear()

    def get_count(self):
        """Get number of enemies"""
        return len(self.enemies)
