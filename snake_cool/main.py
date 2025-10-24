#!/usr/bin/env python3
"""
Snake Cool Game
AssistDigital Leipzig Demo
Created by Claude Code 2 & Claude Sonnet 4.5

Features:
- Intelligent enemy AI with chase/wander behavior
- Epic boss fight with projectile attacks
- Score & Highscore tracking
- Rare banana spawns
- Modern Neon Cyber aesthetic
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game

def main():
    """Entry point for Snake Cool Game"""
    print("=" * 60)
    print("SNAKE COOL - AssistDigital Leipzig Demo")
    print("=" * 60)
    print("\nControls:")
    print("  Arrow Keys - Move snake")
    print("  ESC - Pause/Menu")
    print("  SPACE - Restart (when game over)")
    print("\nObjective:")
    print("  Collect apples (10 pts) and rare bananas (50 pts)")
    print("  Avoid enemies and boss projectiles!")
    print("  Boss spawns at 200 points - defeat it for 100 bonus!")
    print("\nStarting game...")
    print("=" * 60)
    print()

    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nThanks for playing Snake Cool!")
        print("Created live at AssistDigital Leipzig")

if __name__ == "__main__":
    main()
