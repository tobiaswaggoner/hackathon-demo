# UI System for Snake Cool Game
import pygame
from constants import *

class UI:
    def __init__(self):
        """Initialize UI system"""
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def draw_score(self, surface, score):
        """Draw current score (top left)"""
        score_text = f"Score: {score}"
        text_surface = self.font_small.render(score_text, True, UI_TEXT_COLOR)
        surface.blit(text_surface, (20, 20))

    def draw_highscore(self, surface, highscore):
        """Draw highscore (top right)"""
        highscore_text = f"High: {highscore}"
        text_surface = self.font_small.render(highscore_text, True, UI_HIGHLIGHT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topright = (WINDOW_WIDTH - 20, 20)
        surface.blit(text_surface, text_rect)

    def draw_boss_health(self, surface, current_hp, max_hp):
        """Draw boss health bar (top center)"""
        if current_hp <= 0:
            return

        # Background bar
        bar_width = 300
        bar_height = 30
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 20

        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect)

        # Health bar
        health_width = int((current_hp / max_hp) * bar_width)
        health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
        pygame.draw.rect(surface, BOSS_COLOR, health_rect)

        # Border
        pygame.draw.rect(surface, BOSS_GLOW_COLOR, bg_rect, 3)

        # Text
        boss_text = f"BOSS: {current_hp}/{max_hp}"
        text_surface = self.font_small.render(boss_text, True, UI_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, bar_y - 20)
        surface.blit(text_surface, text_rect)

    def draw_game_over(self, surface, final_score, highscore):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, ENEMY_COLOR)
        text_rect = game_over_text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        surface.blit(game_over_text, text_rect)

        # Final score
        score_text = self.font_medium.render(f"Score: {final_score}", True, UI_TEXT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        surface.blit(score_text, score_rect)

        # New highscore?
        if final_score >= highscore:
            new_high_text = self.font_small.render("NEW HIGHSCORE!", True, UI_HIGHLIGHT_COLOR)
            new_high_rect = new_high_text.get_rect()
            new_high_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
            surface.blit(new_high_text, new_high_rect)

        # Instructions
        instruction_text = self.font_small.render("Press SPACE to restart or ESC for menu", True, UI_TEXT_COLOR)
        instruction_rect = instruction_text.get_rect()
        instruction_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150)
        surface.blit(instruction_text, instruction_rect)

    def draw_boss_warning(self, surface):
        """Draw boss spawn warning"""
        warning_text = self.font_large.render("BOSS APPROACHING!", True, BOSS_GLOW_COLOR)
        text_rect = warning_text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        surface.blit(warning_text, text_rect)
