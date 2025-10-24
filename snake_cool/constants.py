# Constants for Snake Cool Game
# AssistDigital Leipzig Demo

import pygame

# Display Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 40
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE  # 30 cells
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE  # 20 cells
FPS = 60

# Colors - Neon Cyber Theme
BACKGROUND_COLOR = (20, 20, 30)
GRID_COLOR = (30, 30, 45)

# Snake Colors
SNAKE_HEAD_COLOR = (50, 220, 150)
SNAKE_BODY_COLOR = (40, 180, 120)
SNAKE_GLOW_COLOR = (100, 255, 200)

# Enemy Colors
ENEMY_COLOR = (220, 50, 50)
ENEMY_GLOW_COLOR = (255, 100, 100)

# Boss Colors
BOSS_COLOR = (180, 0, 80)
BOSS_GLOW_COLOR = (255, 50, 150)

# Food Colors
APPLE_COLOR = (220, 20, 60)
BANANA_COLOR = (255, 215, 0)
BANANA_GLOW_COLOR = (255, 255, 150)

# Projectile Colors
PROJECTILE_COLOR = (255, 100, 0)
PROJECTILE_GLOW_COLOR = (255, 150, 50)

# UI Colors
UI_TEXT_COLOR = (200, 200, 220)
UI_HIGHLIGHT_COLOR = (50, 220, 150)
MENU_BG_COLOR = (30, 30, 45)

# Game Balance
SNAKE_SPEED = 8  # Moves per second
SNAKE_MOVE_DELAY = 1000 // SNAKE_SPEED  # Milliseconds between moves

# Enemy Settings
ENEMY_SPAWN_SCORE = 50
ENEMY_SCORE_INCREMENT = 50  # Spawn additional enemy every 50 points
MAX_ENEMIES = 3
ENEMY_SPEED = 6  # Slightly slower than snake
ENEMY_ACTIVATION_RADIUS = 15  # Cells
ENEMY_DIRECTION_COOLDOWN = 300  # ms

# Boss Settings
BOSS_SPAWN_SCORE = 50
BOSS_HEALTH = 5
BOSS_SPEED = 4
BOSS_SHOOT_INTERVAL = 2000  # ms
BOSS_DEFEAT_BONUS = 100
BOSS_KEEP_DISTANCE = 8  # cells

# Food Settings
BANANA_SPAWN_CHANCE = 0.15  # 15% chance for banana
APPLE_POINTS = 10
BANANA_POINTS = 50

# Projectile Settings
PROJECTILE_SPEED = 5  # pixels per frame

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game States
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'game_over'

# File Paths
HIGHSCORE_FILE = 'snake_cool/highscore.json'
