# Main Game Logic for Snake Cool Game
import pygame
import json
import os
from constants import *
from snake import Snake
from food import FoodManager
from enemy import EnemyManager
from boss import Boss
from projectile import ProjectileManager
from ui import UI
from menu import Menu

class Game:
    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Cool - AssistDigital Leipzig Demo")
        self.clock = pygame.time.Clock()

        # Game state
        self.state = STATE_MENU
        self.running = True

        # Game objects
        self.snake = None
        self.food_manager = None
        self.enemy_manager = None
        self.boss = None
        self.projectile_manager = None

        # Systems
        self.ui = UI()
        self.menu = Menu()

        # Score
        self.score = 0
        self.highscore = self.load_highscore()

        # Boss tracking
        self.boss_spawned = False
        self.boss_warning_time = 0

    def load_highscore(self):
        """Load highscore from file"""
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
        except:
            pass
        return 0

    def save_highscore(self):
        """Save highscore to file"""
        try:
            os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True)
            with open(HIGHSCORE_FILE, 'w') as f:
                json.dump({'highscore': self.highscore}, f)
        except:
            pass

    def reset_game(self):
        """Reset game to initial state"""
        self.snake = Snake()
        self.food_manager = FoodManager()
        self.enemy_manager = EnemyManager()
        self.projectile_manager = ProjectileManager()
        self.boss = None
        self.boss_spawned = False
        self.boss_warning_time = 0
        self.score = 0

        # Spawn initial food
        occupied = set(self.snake.body)
        self.food_manager.spawn_new_food(occupied)

    def handle_events(self):
        """Handle input events"""
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_PLAYING:
                    # Snake controls
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING

                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

            if event.type == pygame.MOUSEMOTION:
                if self.state == STATE_MENU:
                    self.menu.handle_mouse_motion(event.pos, paused=False)
                elif self.state == STATE_PAUSED:
                    self.menu.handle_mouse_motion(event.pos, paused=True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_MENU:
                    action = self.menu.handle_mouse_click(event.pos, paused=False)
                    if action == 'start':
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif action == 'quit':
                        self.running = False

                elif self.state == STATE_PAUSED:
                    action = self.menu.handle_mouse_click(event.pos, paused=True)
                    if action == 'resume':
                        self.state = STATE_PLAYING
                    elif action == 'menu':
                        self.state = STATE_MENU
                    elif action == 'quit':
                        self.running = False

    def update(self):
        """Update game state"""
        if self.state != STATE_PLAYING:
            return

        current_time = pygame.time.get_ticks()

        # Update snake
        self.snake.update(current_time)

        # Check if snake is still alive
        if not self.snake.is_alive():
            self.state = STATE_GAME_OVER
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
            return

        # Update food
        self.food_manager.update()

        # Check food collision
        head = self.snake.get_head()
        ate_food, points = self.food_manager.check_collision(head)
        if ate_food:
            self.score += points
            self.snake.grow()

            # Spawn new food
            occupied = set(self.snake.body)
            occupied.update(self.enemy_manager.get_positions())
            if self.boss and self.boss.is_alive():
                occupied.add(self.boss.get_grid_position())
            self.food_manager.spawn_new_food(occupied)

        # Enemy spawning logic
        enemies_needed = min(self.score // ENEMY_SPAWN_SCORE, MAX_ENEMIES)
        while self.enemy_manager.get_count() < enemies_needed:
            food_pos = self.food_manager.get_position()
            existing = self.enemy_manager.get_positions()
            self.enemy_manager.spawn_enemy(self.snake.body, food_pos, existing)

        # Update enemies
        self.enemy_manager.update(head, self.snake.body, current_time)

        # Check enemy collision
        if self.enemy_manager.check_collision_with_snake(head):
            self.state = STATE_GAME_OVER
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
            return

        # Boss spawning
        if self.score >= BOSS_SPAWN_SCORE and not self.boss_spawned:
            self.boss = Boss()
            self.boss_spawned = True
            self.boss_warning_time = current_time

        # Boss logic
        if self.boss and self.boss.is_alive():
            self.boss.update(head, current_time)

            # Boss shooting
            if self.boss.should_shoot(current_time):
                self.projectile_manager.add_projectile(
                    self.boss.get_position(),
                    head
                )

            # Check if snake body hit boss (damage to boss)
            if self.boss.check_collision_with_snake_body(self.snake.body):
                self.boss.take_damage()
                if not self.boss.is_alive():
                    # Boss defeated!
                    self.score += BOSS_DEFEAT_BONUS
                    self.boss = None

        # Update projectiles
        if self.projectile_manager:
            self.projectile_manager.update()

            # Check projectile collision with snake
            if self.projectile_manager.check_collision_with_snake(self.snake.body):
                self.state = STATE_GAME_OVER
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.save_highscore()
                return

    def draw_background(self):
        """Draw background with grid"""
        self.screen.fill(BACKGROUND_COLOR)

        # Draw subtle grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y), 1)

    def draw(self):
        """Render everything"""
        if self.state == STATE_MENU:
            self.menu.draw_main_menu(self.screen, self.highscore)

        elif self.state == STATE_PLAYING or self.state == STATE_PAUSED or self.state == STATE_GAME_OVER:
            # Draw game
            self.draw_background()

            # Draw game objects
            if self.food_manager:
                self.food_manager.draw(self.screen)

            if self.enemy_manager:
                self.enemy_manager.draw(self.screen)

            if self.boss and self.boss.is_alive():
                self.boss.draw(self.screen)

            if self.projectile_manager:
                self.projectile_manager.draw(self.screen)

            if self.snake:
                self.snake.draw(self.screen)

            # Draw UI
            self.ui.draw_score(self.screen, self.score)
            self.ui.draw_highscore(self.screen, self.highscore)

            if self.boss and self.boss.is_alive():
                self.ui.draw_boss_health(self.screen, self.boss.health, self.boss.max_health)

            # Boss warning
            current_time = pygame.time.get_ticks()
            if self.boss_warning_time > 0 and current_time - self.boss_warning_time < 2000:
                self.ui.draw_boss_warning(self.screen)

            # Pause overlay
            if self.state == STATE_PAUSED:
                self.menu.draw_pause_menu(self.screen)

            # Game over overlay
            if self.state == STATE_GAME_OVER:
                self.ui.draw_game_over(self.screen, self.score, self.highscore)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
