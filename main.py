import sys
import random
import pygame

# Simple Snake game using pygame
# Controls:
#   Arrow keys or WASD to move
#   R to restart after game over
#   ESC or window close to quit

# --- Configuration ---
TILE_SIZE = 20
GRID_WIDTH = 30   # columns
GRID_HEIGHT = 20  # rows
FPS = 12          # snake speed (frames per second)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 0, 0)
GRAY = (40, 40, 40)

# Directions as (dx, dy)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_empty_cell(snake):
    """Return a random grid position not occupied by the snake."""
    occupied = set(snake)
    while True:
        p = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        if p not in occupied:
            return p


def draw_grid(surface):
    """Draw a subtle grid background."""
    for x in range(0, GRID_WIDTH * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, GRID_HEIGHT * TILE_SIZE))
    for y in range(0, GRID_HEIGHT * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (GRID_WIDTH * TILE_SIZE, y))


def draw_rect(surface, color, cell):
    x, y = cell
    r = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface, color, r)


def opposite_dir(a, b):
    return a[0] == -b[0] and a[1] == -b[1]


def run_game(screen, clock, font):
    # Initialize snake in center with length 3 moving right
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
    direction = RIGHT
    pending_dir = RIGHT

    apple = random_empty_cell(snake)
    score = 0

    alive = True

    while True:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    pygame.quit()
                    sys.exit(0)
                if alive:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        if not opposite_dir(direction, UP):
                            pending_dir = UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        if not opposite_dir(direction, DOWN):
                            pending_dir = DOWN
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if not opposite_dir(direction, LEFT):
                            pending_dir = LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if not opposite_dir(direction, RIGHT):
                            pending_dir = RIGHT
                else:
                    if event.key in (pygame.K_r,):
                        # Restart
                        return 'restart'

        if alive:
            direction = pending_dir
            # Move snake: add new head based on direction
            head_x, head_y = snake[-1]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Check collisions with walls
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                alive = False
            # Check collisions with self
            elif new_head in snake:
                alive = False
            else:
                snake.append(new_head)
                # Apple check
                if new_head == apple:
                    score += 1
                    apple = random_empty_cell(snake)
                else:
                    # move tail
                    snake.pop(0)

        # Render
        screen.fill(BLACK)
        draw_grid(screen)

        # Draw apple
        draw_rect(screen, RED, apple)

        # Draw snake (head darker)
        for i, cell in enumerate(snake):
            color = DARK_GREEN if i == len(snake) - 1 else GREEN
            draw_rect(screen, color, cell)

        # HUD
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (8, 6))

        if not alive:
            over_text = font.render("Game Over - Press R to restart", True, WHITE)
            rect = over_text.get_rect(center=(GRID_WIDTH * TILE_SIZE // 2, GRID_HEIGHT * TILE_SIZE // 2))
            screen.blit(over_text, rect)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.set_caption("Snake (pygame) - Minimal")

    screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    while True:
        result = run_game(screen, clock, font)
        if result != 'restart':
            break


if __name__ == "__main__":
    main()
