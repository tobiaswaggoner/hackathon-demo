# Game Configuration
# All constants and settings for the Snake Game

import pygame

# Window Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Grid Settings
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE  # 60 cells
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 40 cells

# Colors (Hex to RGB)
COLOR_BACKGROUND = (26, 26, 26)  # #1a1a1a
COLOR_SNAKE_HEAD = (0, 255, 0)  # #00ff00
COLOR_SNAKE_BODY = (0, 170, 0)  # #00aa00
COLOR_FOOD = (255, 0, 0)  # #ff0000
COLOR_BONUS_FOOD = (255, 215, 0)  # #ffd700
COLOR_ENEMY = (255, 102, 0)  # #ff6600
COLOR_BOSS = (139, 0, 0)  # #8b0000
COLOR_PROJECTILE = (255, 51, 51)  # #ff3333
COLOR_TEXT = (255, 255, 255)  # White
COLOR_TEXT_SHADOW = (50, 50, 50)  # Dark gray

# Snake Settings
SNAKE_SPEED = 10  # Moves per second
SNAKE_INITIAL_LENGTH = 3

# Food Settings
FOOD_NORMAL_SCORE = 10
FOOD_BONUS_SCORE = 50
FOOD_NORMAL_GROWTH = 1
FOOD_BONUS_GROWTH = 3
BONUS_FOOD_CHANCE = 0.05  # 5% chance

# Enemy Settings
ENEMY_SPEED = 0.6  # Relative to snake (60% speed)
ENEMY_HEALTH = 3
ENEMY_SCORE = 100
ENEMY_DETECTION_RANGE = 300  # Pixels
ENEMY_CLOSE_RANGE = 50  # Pixels
ENEMY_AI_ERROR_CHANCE = 0.2  # 20% chance to make wrong decision
ENEMY_AI_DELAY = 0.3  # Reaction time in seconds
ENEMY_EVADE_THRESHOLD = 15  # Snake segments
ENEMY_SHOOT_COOLDOWN = 3.0  # Seconds between shots

# Enemy Spawning
ENEMY_FIRST_WAVE_TIME = 10.0  # Seconds
ENEMY_WAVE_INTERVAL = 20.0  # Seconds
ENEMY_MAX_CONCURRENT = 5
ENEMY_MIN_SPAWN_DISTANCE = 300  # From snake
ENEMY_MIN_ENEMY_DISTANCE = 100  # From other enemies

# Boss Settings
BOSS_SPAWN_SCORE = 500
BOSS_SIZE = 5  # Grid cells (5x5 = 100x100 pixels)
BOSS_HEALTH = 20
BOSS_SPEED = 0.3  # Relative to snake
BOSS_SCORE = 500
BOSS_SHOOT_COOLDOWN = 1.5  # Seconds
BOSS_MIN_DISTANCE = 150  # Pixels
BOSS_MAX_DISTANCE = 400  # Pixels
BOSS_PROJECTILES_PER_SHOT = 3
BOSS_PROJECTILE_SPREAD = 15  # Degrees

# Projectile Settings
PROJECTILE_SPEED = 5.0  # Pixels per frame
PROJECTILE_RADIUS = 5

# Game States
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
STATE_BOSS_INTRO = "BOSS_INTRO"

# UI Settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Game Feel Settings
BOSS_INTRO_DURATION = 3.0  # Seconds
VICTORY_SCREEN_DURATION = 3.0  # Seconds
