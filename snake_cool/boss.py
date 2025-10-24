# Boss System for Snake Cool Game
import pygame
import math
import random
from constants import *

class Boss:
    def __init__(self):
        """Initialize boss at center"""
        self.position = [GRID_WIDTH // 2, GRID_HEIGHT // 2]
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.last_shot_time = 0
        self.animation_offset = 0
        self.orbit_angle = 0

        # Boss is larger than regular enemies
        self.size_multiplier = 2

    def update(self, snake_head_pos, current_time):
        """Update boss AI and position"""
        head_x, head_y = snake_head_pos

        # Calculate distance to snake
        distance = math.sqrt(
            (self.position[0] - head_x) ** 2 +
            (self.position[1] - head_y) ** 2
        )

        # Movement strategy: Orbit the snake while maintaining distance
        if distance < BOSS_KEEP_DISTANCE - 2:
            # Too close, move away
            dx = self.position[0] - head_x
            dy = self.position[1] - head_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                move_x = dx / dist
                move_y = dy / dist
        elif distance > BOSS_KEEP_DISTANCE + 2:
            # Too far, move closer
            dx = head_x - self.position[0]
            dy = head_y - self.position[1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                move_x = dx / dist
                move_y = dy / dist
        else:
            # Good distance, orbit around snake
            self.orbit_angle += 0.03
            # Calculate perpendicular movement
            to_snake_x = head_x - self.position[0]
            to_snake_y = head_y - self.position[1]
            # Rotate 90 degrees for orbit
            move_x = -to_snake_y
            move_y = to_snake_x
            dist = math.sqrt(move_x * move_x + move_y * move_y)
            if dist > 0:
                move_x = move_x / dist
                move_y = move_y / dist

        # Apply movement (slower than regular enemies)
        new_x = self.position[0] + move_x * 0.3
        new_y = self.position[1] + move_y * 0.3

        # Keep in bounds
        new_x = max(1, min(GRID_WIDTH - 2, new_x))
        new_y = max(1, min(GRID_HEIGHT - 2, new_y))

        self.position = [new_x, new_y]

        # Update animation
        self.animation_offset += 0.1

    def should_shoot(self, current_time):
        """Check if boss should shoot"""
        if current_time - self.last_shot_time >= BOSS_SHOOT_INTERVAL:
            self.last_shot_time = current_time
            return True
        return False

    def get_position(self):
        """Get boss position as tuple"""
        return tuple(self.position)

    def get_grid_position(self):
        """Get integer grid position"""
        return (int(self.position[0]), int(self.position[1]))

    def take_damage(self):
        """Boss takes damage"""
        self.health -= 1

    def is_alive(self):
        """Check if boss is alive"""
        return self.health > 0

    def get_health_percentage(self):
        """Get health as percentage"""
        return self.health / self.max_health

    def draw(self, surface):
        """Draw boss with impressive effects"""
        x, y = self.position
        pixel_x = int(x * CELL_SIZE)
        pixel_y = int(y * CELL_SIZE)

        boss_size = CELL_SIZE * self.size_multiplier

        # Intense pulsing glow
        pulse = math.sin(self.animation_offset * 2) * 0.3 + 0.7

        # Multiple glow layers for impressive effect
        for i in range(5):
            glow_size = boss_size + 20 - i * 3
            glow_offset = (boss_size - glow_size) // 2
            glow_alpha = int((200 - i * 40) * pulse)

            glow_rect = pygame.Rect(
                pixel_x + glow_offset,
                pixel_y + glow_offset,
                glow_size, glow_size
            )

            # Create alpha surface for glow
            alpha_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            color_with_alpha = (*BOSS_GLOW_COLOR, glow_alpha)
            pygame.draw.rect(alpha_surface, color_with_alpha,
                           alpha_surface.get_rect(), border_radius=10)
            surface.blit(alpha_surface, (pixel_x + glow_offset, pixel_y + glow_offset))

        # Main boss body
        boss_rect = pygame.Rect(pixel_x, pixel_y, boss_size, boss_size)
        pygame.draw.rect(surface, BOSS_COLOR, boss_rect, border_radius=8)

        # Animated border
        border_color = tuple(int(c * pulse) for c in BOSS_GLOW_COLOR)
        pygame.draw.rect(surface, border_color, boss_rect, 4, border_radius=8)

        # Eyes or core pattern
        center_x = pixel_x + boss_size // 2
        center_y = pixel_y + boss_size // 2

        # Rotating energy core
        core_radius = int(15 * pulse)
        pygame.draw.circle(surface, BOSS_GLOW_COLOR, (center_x, center_y), core_radius)
        pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), core_radius // 2)

        # Angry eyes
        eye_offset_x = boss_size // 3
        eye_offset_y = boss_size // 4
        eye_color = (255, 50, 50)
        eye_size = 6

        left_eye = (pixel_x + eye_offset_x, pixel_y + eye_offset_y)
        right_eye = (pixel_x + boss_size - eye_offset_x, pixel_y + eye_offset_y)

        pygame.draw.circle(surface, eye_color, left_eye, eye_size)
        pygame.draw.circle(surface, eye_color, right_eye, eye_size)

        # Pupil glow
        pygame.draw.circle(surface, (255, 255, 0), left_eye, eye_size // 2)
        pygame.draw.circle(surface, (255, 255, 0), right_eye, eye_size // 2)

    def check_collision_with_snake_body(self, snake_body):
        """Check if snake body hit the boss (damage to boss)"""
        grid_pos = self.get_grid_position()

        # Boss occupies 2x2 cells
        boss_cells = [
            grid_pos,
            (grid_pos[0] + 1, grid_pos[1]),
            (grid_pos[0], grid_pos[1] + 1),
            (grid_pos[0] + 1, grid_pos[1] + 1)
        ]

        for cell in boss_cells:
            if cell in snake_body:
                return True
        return False
