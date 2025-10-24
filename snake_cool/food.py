# Food System for Snake Cool Game
import pygame
import random
import math
from constants import *

class Food:
    def __init__(self, food_type='apple'):
        """Initialize food item"""
        self.type = food_type  # 'apple' or 'banana'
        self.position = (0, 0)
        self.animation_offset = 0

    def spawn(self, occupied_cells):
        """Spawn food at random unoccupied position"""
        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if (x, y) not in occupied_cells:
                self.position = (x, y)
                return True

            attempts += 1

        # Fallback: spawn anywhere
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
        return True

    def get_points(self):
        """Return points for this food type"""
        if self.type == 'banana':
            return BANANA_POINTS
        return APPLE_POINTS

    def update(self):
        """Update animation"""
        self.animation_offset += 0.1

    def draw(self, surface):
        """Draw food with effects"""
        x, y = self.position
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE

        # Animation: slight pulsing
        pulse = math.sin(self.animation_offset) * 2
        size_offset = int(pulse)

        if self.type == 'banana':
            # Banana - with glow effect (rare item!)
            # Outer glow
            for i in range(3):
                glow_size = CELL_SIZE + 8 - i * 2
                glow_offset = (CELL_SIZE - glow_size) // 2
                glow_rect = pygame.Rect(
                    pixel_x + glow_offset,
                    pixel_y + glow_offset,
                    glow_size, glow_size
                )
                alpha_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                alpha = 100 - i * 30
                color_with_alpha = (*BANANA_GLOW_COLOR, alpha)
                pygame.draw.rect(alpha_surface, color_with_alpha, alpha_surface.get_rect(), border_radius=8)
                surface.blit(alpha_surface, (pixel_x + glow_offset, pixel_y + glow_offset))

            # Main banana
            banana_rect = pygame.Rect(
                pixel_x - size_offset,
                pixel_y - size_offset,
                CELL_SIZE + size_offset * 2,
                CELL_SIZE + size_offset * 2
            )
            pygame.draw.rect(surface, BANANA_COLOR, banana_rect, border_radius=8)
            pygame.draw.rect(surface, BANANA_GLOW_COLOR, banana_rect, 3, border_radius=8)

            # Sparkle effect
            if int(self.animation_offset * 10) % 20 < 10:
                sparkle_x = pixel_x + CELL_SIZE // 2
                sparkle_y = pixel_y + CELL_SIZE // 4
                pygame.draw.circle(surface, (255, 255, 255), (sparkle_x, sparkle_y), 3)

        else:
            # Apple - simpler
            apple_rect = pygame.Rect(
                pixel_x - size_offset,
                pixel_y - size_offset,
                CELL_SIZE + size_offset * 2,
                CELL_SIZE + size_offset * 2
            )
            pygame.draw.rect(surface, APPLE_COLOR, apple_rect, border_radius=6)
            pygame.draw.rect(surface, (255, 100, 100), apple_rect, 2, border_radius=6)


class FoodManager:
    def __init__(self):
        """Manage food spawning"""
        self.current_food = None

    def spawn_new_food(self, occupied_cells):
        """Spawn new food (apple or rare banana)"""
        # Determine type
        if random.random() < BANANA_SPAWN_CHANCE:
            food_type = 'banana'
        else:
            food_type = 'apple'

        self.current_food = Food(food_type)
        self.current_food.spawn(occupied_cells)

    def update(self):
        """Update current food"""
        if self.current_food:
            self.current_food.update()

    def draw(self, surface):
        """Draw current food"""
        if self.current_food:
            self.current_food.draw(surface)

    def check_collision(self, position):
        """Check if position collides with food"""
        if self.current_food and self.current_food.position == position:
            points = self.current_food.get_points()
            return True, points
        return False, 0

    def get_position(self):
        """Get current food position"""
        if self.current_food:
            return self.current_food.position
        return None
