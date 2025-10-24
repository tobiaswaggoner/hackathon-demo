# Menu System for Snake Cool Game
import pygame
from constants import *

class MenuItem:
    def __init__(self, text, y_position, action):
        """Menu item with hover effect"""
        self.text = text
        self.y_position = y_position
        self.action = action
        self.hovered = False

    def check_hover(self, mouse_pos):
        """Check if mouse is hovering"""
        # Approximate text bounds
        text_width = len(self.text) * 20
        text_height = 40
        x = WINDOW_WIDTH // 2 - text_width // 2
        y = self.y_position - text_height // 2

        rect = pygame.Rect(x, y, text_width, text_height)
        self.hovered = rect.collidepoint(mouse_pos)
        return self.hovered

    def draw(self, surface, font):
        """Draw menu item"""
        color = UI_HIGHLIGHT_COLOR if self.hovered else UI_TEXT_COLOR
        text_surface = font.render(self.text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, self.y_position)
        surface.blit(text_surface, text_rect)

        # Glow effect when hovered
        if self.hovered:
            glow_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(surface, UI_HIGHLIGHT_COLOR, glow_rect, 2)


class Menu:
    def __init__(self):
        """Initialize menu system"""
        pygame.font.init()
        self.font_title = pygame.font.Font(None, 96)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # Main menu items
        self.main_menu_items = [
            MenuItem("Start Game", WINDOW_HEIGHT // 2, "start"),
            MenuItem("Quit", WINDOW_HEIGHT // 2 + 80, "quit")
        ]

        # Pause menu items
        self.pause_menu_items = [
            MenuItem("Resume", WINDOW_HEIGHT // 2, "resume"),
            MenuItem("Main Menu", WINDOW_HEIGHT // 2 + 80, "menu"),
            MenuItem("Quit", WINDOW_HEIGHT // 2 + 160, "quit")
        ]

        self.selected_action = None

    def draw_main_menu(self, surface, highscore):
        """Draw main menu"""
        # Background
        surface.fill(BACKGROUND_COLOR)

        # Title
        title_text = self.font_title.render("SNAKE COOL", True, SNAKE_HEAD_COLOR)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH // 2, 150)
        surface.blit(title_text, title_rect)

        # Title glow
        glow_rect = title_rect.inflate(20, 10)
        pygame.draw.rect(surface, SNAKE_GLOW_COLOR, glow_rect, 3)

        # Subtitle
        subtitle_text = self.font_small.render("AssistDigital Leipzig Demo", True, UI_TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect()
        subtitle_rect.center = (WINDOW_WIDTH // 2, 220)
        surface.blit(subtitle_text, subtitle_rect)

        # Highscore
        highscore_text = self.font_menu.render(f"Highscore: {highscore}", True, UI_HIGHLIGHT_COLOR)
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (WINDOW_WIDTH // 2, 300)
        surface.blit(highscore_text, highscore_rect)

        # Menu items
        for item in self.main_menu_items:
            item.draw(surface, self.font_menu)

        # Controls info
        controls_y = WINDOW_HEIGHT - 100
        controls = [
            "Controls: Arrow Keys to move",
            "ESC to pause | Collect apples and rare bananas!",
            "Avoid enemies and boss projectiles!"
        ]

        for i, control_text in enumerate(controls):
            text_surface = self.font_small.render(control_text, True, UI_TEXT_COLOR)
            text_rect = text_surface.get_rect()
            text_rect.center = (WINDOW_WIDTH // 2, controls_y + i * 30)
            surface.blit(text_surface, text_rect)

    def draw_pause_menu(self, surface):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Paused text
        paused_text = self.font_title.render("PAUSED", True, UI_HIGHLIGHT_COLOR)
        paused_rect = paused_text.get_rect()
        paused_rect.center = (WINDOW_WIDTH // 2, 200)
        surface.blit(paused_text, paused_rect)

        # Menu items
        for item in self.pause_menu_items:
            item.draw(surface, self.font_menu)

    def handle_mouse_motion(self, mouse_pos, paused=False):
        """Handle mouse movement"""
        items = self.pause_menu_items if paused else self.main_menu_items
        for item in items:
            item.check_hover(mouse_pos)

    def handle_mouse_click(self, mouse_pos, paused=False):
        """Handle mouse click"""
        items = self.pause_menu_items if paused else self.main_menu_items
        for item in items:
            if item.check_hover(mouse_pos):
                self.selected_action = item.action
                return item.action
        return None

    def get_selected_action(self):
        """Get and clear selected action"""
        action = self.selected_action
        self.selected_action = None
        return action
