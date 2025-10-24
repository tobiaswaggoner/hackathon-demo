# Snake Class for Snake Cool Game
import pygame
from constants import *

class Snake:
    def __init__(self):
        """Initialize snake at center of screen"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Snake body as list of (x, y) grid positions
        self.body = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]

        self.direction = RIGHT
        self.next_direction = RIGHT  # Input buffer
        self.grow_pending = 0

        # Movement timing
        self.last_move_time = 0

    def change_direction(self, new_direction):
        """Buffer direction change (prevents opposite direction)"""
        # Can't reverse into yourself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def update(self, current_time):
        """Update snake position based on timing"""
        if current_time - self.last_move_time >= SNAKE_MOVE_DELAY:
            self.move()
            self.last_move_time = current_time

    def move(self):
        """Move snake one cell in current direction"""
        # Apply buffered direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, segments=1):
        """Schedule growth"""
        self.grow_pending += segments

    def get_head(self):
        """Get head position"""
        return self.body[0]

    def get_body_without_head(self):
        """Get body segments excluding head"""
        return self.body[1:]

    def check_wall_collision(self):
        """Check if snake hit a wall"""
        head_x, head_y = self.get_head()
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT

    def check_self_collision(self):
        """Check if snake hit itself"""
        head = self.get_head()
        return head in self.body[1:]

    def is_alive(self):
        """Check if snake is still alive"""
        return not (self.check_wall_collision() or self.check_self_collision())

    def draw(self, surface):
        """Draw snake with gradient effect"""
        for i, (x, y) in enumerate(self.body):
            pixel_x = x * CELL_SIZE
            pixel_y = y * CELL_SIZE

            if i == 0:
                # Head - brighter with glow
                # Draw glow effect
                glow_rect = pygame.Rect(
                    pixel_x - 2, pixel_y - 2,
                    CELL_SIZE + 4, CELL_SIZE + 4
                )
                pygame.draw.rect(surface, SNAKE_GLOW_COLOR, glow_rect, 2)

                # Draw head
                head_rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, head_rect)
                pygame.draw.rect(surface, SNAKE_GLOW_COLOR, head_rect, 2)
            else:
                # Body - gradient based on position
                fade_factor = 1 - (i / len(self.body)) * 0.3
                color = tuple(int(c * fade_factor) for c in SNAKE_BODY_COLOR)

                body_rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, color, body_rect)
                pygame.draw.rect(surface, SNAKE_BODY_COLOR, body_rect, 1)
