# Projectile System for Snake Cool Game
import pygame
import math
from constants import *

class Projectile:
    def __init__(self, start_pos, target_pos):
        """Initialize projectile from start to target"""
        # Convert grid to pixel coordinates
        self.x = start_pos[0] * CELL_SIZE + CELL_SIZE // 2
        self.y = start_pos[1] * CELL_SIZE + CELL_SIZE // 2

        target_x = target_pos[0] * CELL_SIZE + CELL_SIZE // 2
        target_y = target_pos[1] * CELL_SIZE + CELL_SIZE // 2

        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.velocity_x = (dx / distance) * PROJECTILE_SPEED
            self.velocity_y = (dy / distance) * PROJECTILE_SPEED
        else:
            self.velocity_x = 0
            self.velocity_y = 0

        self.radius = 8
        self.animation_offset = 0

    def update(self):
        """Update projectile position"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.animation_offset += 0.2

    def is_off_screen(self):
        """Check if projectile is off screen"""
        return (self.x < -50 or self.x > WINDOW_WIDTH + 50 or
                self.y < -50 or self.y > WINDOW_HEIGHT + 50)

    def check_collision_with_snake(self, snake_segments):
        """Check collision with snake (only head matters)"""
        head_x, head_y = snake_segments[0]
        head_pixel_x = head_x * CELL_SIZE + CELL_SIZE // 2
        head_pixel_y = head_y * CELL_SIZE + CELL_SIZE // 2

        # Distance to head
        dx = self.x - head_pixel_x
        dy = self.y - head_pixel_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision if within cell size
        return distance < CELL_SIZE // 2 + self.radius

    def draw(self, surface):
        """Draw projectile with glow effect"""
        # Pulsing glow
        pulse = math.sin(self.animation_offset) * 0.3 + 0.7

        # Multiple glow layers
        for i in range(3):
            glow_radius = int((self.radius + 8 - i * 2) * pulse)
            glow_color = tuple(int(c * (pulse * 0.5 + 0.5)) for c in PROJECTILE_GLOW_COLOR)
            pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), glow_radius)

        # Main projectile
        pygame.draw.circle(surface, PROJECTILE_COLOR, (int(self.x), int(self.y)), self.radius)

        # Bright core
        core_color = (255, 200, 100)
        pygame.draw.circle(surface, core_color, (int(self.x), int(self.y)), self.radius // 2)


class ProjectileManager:
    def __init__(self):
        """Manage all projectiles"""
        self.projectiles = []

    def add_projectile(self, start_pos, target_pos):
        """Add new projectile"""
        projectile = Projectile(start_pos, target_pos)
        self.projectiles.append(projectile)

    def update(self):
        """Update all projectiles"""
        # Update positions
        for projectile in self.projectiles:
            projectile.update()

        # Remove off-screen projectiles
        self.projectiles = [p for p in self.projectiles if not p.is_off_screen()]

    def check_collision_with_snake(self, snake_segments):
        """Check if any projectile hit the snake"""
        for projectile in self.projectiles:
            if projectile.check_collision_with_snake(snake_segments):
                self.projectiles.remove(projectile)
                return True
        return False

    def draw(self, surface):
        """Draw all projectiles"""
        for projectile in self.projectiles:
            projectile.draw(surface)

    def clear(self):
        """Remove all projectiles"""
        self.projectiles.clear()

    def get_count(self):
        """Get number of active projectiles"""
        return len(self.projectiles)
