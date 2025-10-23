# Snake Game - Main Game Loop
# Extended Snake Game with AI Enemies and Boss Fights

import pygame
import sys
import random
import math
from config import *
from game_objects import Snake, Food, Enemy, Boss, Projectile
from score_manager import ScoreManager
from ai_behavior import should_enemy_shoot, should_boss_shoot, get_enemy_shoot_angle, get_boss_shoot_angles


class SnakeGame:
    """Main game class with game loop"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - AI Edition")

        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

        self.state = STATE_MENU
        self.reset_game()

    def reset_game(self):
        """Reset game state for new game"""
        self.snake = Snake()
        self.food = Food()
        self.enemies = []
        self.boss = None
        self.projectiles = []
        self.score_manager = ScoreManager()

        # Timing
        self.game_time = 0
        self.last_snake_move = 0
        self.wave_timer = 0
        self.current_wave = 0
        self.boss_intro_timer = 0
        self.boss_defeated_timer = 0

        # Flags
        self.boss_active = False
        self.boss_triggered_at_score = 0

    def run(self):
        """Main game loop"""
        running = True

        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.handle_input(event)

            # Update game state
            if self.state == STATE_PLAYING:
                self.update(dt)
            elif self.state == STATE_BOSS_INTRO:
                self.update_boss_intro(dt)

            # Render
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type != pygame.KEYDOWN:
            return

        # Menu state
        if self.state == STATE_MENU:
            if event.key == pygame.K_SPACE:
                self.state = STATE_PLAYING
                self.reset_game()

        # Playing state
        elif self.state == STATE_PLAYING:
            if event.key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED
            # Snake movement
            elif event.key in [pygame.K_UP, pygame.K_w]:
                self.snake.update_direction([0, -1])
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.snake.update_direction([0, 1])
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.snake.update_direction([-1, 0])
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.snake.update_direction([1, 0])

        # Paused state
        elif self.state == STATE_PAUSED:
            if event.key == pygame.K_ESCAPE:
                self.state = STATE_PLAYING
            elif event.key == pygame.K_q:
                self.state = STATE_MENU

        # Game over state
        elif self.state == STATE_GAME_OVER:
            if event.key == pygame.K_SPACE:
                self.state = STATE_MENU

    def update(self, dt):
        """Update game logic"""
        self.game_time += dt

        # Move snake at fixed rate
        move_interval = 1.0 / SNAKE_SPEED
        if self.game_time - self.last_snake_move >= move_interval:
            self.snake.move()
            self.last_snake_move = self.game_time

            # Check snake collision
            if self.snake.check_collision():
                self.state = STATE_GAME_OVER
                return

        # Check food collision
        if self.snake.segments[0] == self.food.position:
            self.snake.grow(self.food.growth_value)
            self.score_manager.add_score(self.food.score_value)
            self.food.respawn(self.snake.segments, self.enemies)

        # Check for boss spawn
        if not self.boss_active and self.score_manager.score >= BOSS_SPAWN_SCORE:
            score_milestone = (self.score_manager.score // BOSS_SPAWN_SCORE) * BOSS_SPAWN_SCORE
            if score_milestone > self.boss_triggered_at_score:
                self.boss_triggered_at_score = score_milestone
                self.state = STATE_BOSS_INTRO
                self.boss_intro_timer = 0
                return

        # Enemy spawning (only if no boss active)
        if not self.boss_active:
            self.update_enemy_spawning(dt)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.snake, self.enemies)

            # Check if enemy should shoot
            if should_enemy_shoot(enemy):
                angle = get_enemy_shoot_angle(enemy, self.snake)
                self.projectiles.append(Projectile(enemy.x, enemy.y, angle))

            # Check collision with snake head
            head_x, head_y = self.snake.get_head_pos()
            distance = math.sqrt((enemy.x - head_x)**2 + (enemy.y - head_y)**2)
            if distance < GRID_SIZE:
                if enemy.take_damage(1):
                    self.enemies.remove(enemy)
                    self.score_manager.add_score(ENEMY_SCORE)

        # Update boss
        if self.boss:
            self.boss.update(dt, self.snake)

            # Boss shooting
            if should_boss_shoot(self.boss):
                angles = get_boss_shoot_angles(self.boss, self.snake)
                for angle in angles:
                    self.projectiles.append(Projectile(self.boss.x, self.boss.y, angle))

            # Check collision with snake head
            head_x, head_y = self.snake.get_head_pos()
            distance = math.sqrt((self.boss.x - head_x)**2 + (self.boss.y - head_y)**2)
            boss_radius = BOSS_SIZE * GRID_SIZE / 2
            if distance < boss_radius + GRID_SIZE / 2:
                if self.boss.take_damage(1):
                    self.score_manager.add_score(BOSS_SCORE)
                    self.boss = None
                    self.boss_active = False
                    self.boss_defeated_timer = VICTORY_SCREEN_DURATION
                    # Clear all projectiles
                    self.projectiles.clear()

        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()

            # Remove if off screen
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)
                continue

            # Check collision with snake
            if projectile.check_collision(self.snake):
                self.state = STATE_GAME_OVER
                return

    def update_boss_intro(self, dt):
        """Update boss intro sequence"""
        self.boss_intro_timer += dt

        if self.boss_intro_timer >= BOSS_INTRO_DURATION:
            # Spawn boss
            self.boss = Boss()
            self.boss_active = True
            # Remove all enemies
            self.enemies.clear()
            self.projectiles.clear()
            # Return to playing
            self.state = STATE_PLAYING

    def update_enemy_spawning(self, dt):
        """Handle enemy wave spawning"""
        self.wave_timer += dt

        # First wave
        if self.current_wave == 0 and self.game_time >= ENEMY_FIRST_WAVE_TIME:
            self.spawn_enemies(1)
            self.current_wave = 1
            self.wave_timer = 0

        # Subsequent waves
        elif self.current_wave > 0 and self.wave_timer >= ENEMY_WAVE_INTERVAL:
            enemies_to_spawn = min(self.current_wave + 1, ENEMY_MAX_CONCURRENT - len(self.enemies))
            if enemies_to_spawn > 0:
                self.spawn_enemies(enemies_to_spawn)
            self.current_wave += 1
            self.wave_timer = 0

    def spawn_enemies(self, count):
        """Spawn enemies at valid locations"""
        snake_head_x, snake_head_y = self.snake.get_head_pos()

        for _ in range(count):
            if len(self.enemies) >= ENEMY_MAX_CONCURRENT:
                break

            # Find valid spawn location
            max_attempts = 50
            for _ in range(max_attempts):
                # Spawn at edge of screen
                side = random.choice(['top', 'bottom', 'left', 'right'])
                if side == 'top':
                    x = random.randint(50, WINDOW_WIDTH - 50)
                    y = 50
                elif side == 'bottom':
                    x = random.randint(50, WINDOW_WIDTH - 50)
                    y = WINDOW_HEIGHT - 50
                elif side == 'left':
                    x = 50
                    y = random.randint(50, WINDOW_HEIGHT - 50)
                else:  # right
                    x = WINDOW_WIDTH - 50
                    y = random.randint(50, WINDOW_HEIGHT - 50)

                # Check distance from snake
                distance_to_snake = math.sqrt((x - snake_head_x)**2 + (y - snake_head_y)**2)
                if distance_to_snake < ENEMY_MIN_SPAWN_DISTANCE:
                    continue

                # Check distance from other enemies
                too_close = False
                for enemy in self.enemies:
                    distance = math.sqrt((x - enemy.x)**2 + (y - enemy.y)**2)
                    if distance < ENEMY_MIN_ENEMY_DISTANCE:
                        too_close = True
                        break

                if not too_close:
                    self.enemies.append(Enemy(x, y))
                    break

    def draw(self):
        """Render everything"""
        self.screen.fill(COLOR_BACKGROUND)

        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        elif self.state == STATE_PAUSED:
            self.draw_playing()
            self.draw_paused()
        elif self.state == STATE_GAME_OVER:
            self.draw_playing()
            self.draw_game_over()
        elif self.state == STATE_BOSS_INTRO:
            self.draw_playing()
            self.draw_boss_intro()

    def draw_menu(self):
        """Draw main menu"""
        title = self.font_large.render("SNAKE GAME", True, COLOR_SNAKE_HEAD)
        subtitle = self.font_medium.render("AI Edition", True, COLOR_TEXT)
        instruction = self.font_small.render("Press SPACE to Start", True, COLOR_TEXT)
        highscore_text = self.font_small.render(
            f"Highscore: {self.score_manager.get_highscore()}",
            True, COLOR_BONUS_FOOD
        )

        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 270))
        self.screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 400))
        self.screen.blit(highscore_text, (WINDOW_WIDTH // 2 - highscore_text.get_width() // 2, 500))

        # Draw controls
        controls = [
            "Controls:",
            "Arrow Keys / WASD - Move",
            "ESC - Pause",
            "Q - Quit to Menu"
        ]
        y_offset = 550
        for line in controls:
            text = self.font_small.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 30

    def draw_playing(self):
        """Draw game objects"""
        # Draw food
        self.food.draw(self.screen)

        # Draw snake
        self.snake.draw(self.screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw boss
        if self.boss:
            self.boss.draw(self.screen)

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)

        # Draw UI
        self.draw_ui()

    def draw_ui(self):
        """Draw score and other UI elements"""
        # Current score (top-left)
        score_text = self.font_medium.render(f"Score: {self.score_manager.get_score()}", True, COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))

        # Highscore (top-right)
        highscore_text = self.font_small.render(
            f"Best: {self.score_manager.get_highscore()}",
            True, COLOR_BONUS_FOOD
        )
        self.screen.blit(highscore_text, (WINDOW_WIDTH - highscore_text.get_width() - 10, 10))

        # Wave number (top-center)
        if not self.boss_active:
            wave_text = self.font_small.render(f"Wave {self.current_wave}", True, COLOR_TEXT)
            self.screen.blit(wave_text, (WINDOW_WIDTH // 2 - wave_text.get_width() // 2, 10))
        else:
            boss_text = self.font_medium.render("BOSS FIGHT!", True, COLOR_BOSS)
            self.screen.blit(boss_text, (WINDOW_WIDTH // 2 - boss_text.get_width() // 2, 10))

    def draw_paused(self):
        """Draw pause overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("PAUSED", True, COLOR_TEXT)
        instruction = self.font_small.render("Press ESC to Resume, Q to Quit", True, COLOR_TEXT)

        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, WINDOW_HEIGHT // 2 + 20))

    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        text = self.font_large.render("GAME OVER", True, COLOR_FOOD)
        score_text = self.font_medium.render(
            f"Final Score: {self.score_manager.get_score()}",
            True, COLOR_TEXT
        )
        instruction = self.font_small.render("Press SPACE to Continue", True, COLOR_TEXT)

        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, WINDOW_HEIGHT // 2 + 40))

    def draw_boss_intro(self):
        """Draw boss introduction sequence"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Pulsing text effect
        pulse = abs(math.sin(self.boss_intro_timer * 3)) * 30 + 30
        color = (255, int(pulse), int(pulse))

        text = self.font_large.render("BOSS APPEARS!", True, color)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 30))


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
