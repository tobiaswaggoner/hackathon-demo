# Snake Cool Game

**Created live at AssistDigital Leipzig Demo**
*Powered by Claude Code 2 & Claude Sonnet 4.5*

## About

A modern take on the classic Snake game with:
- Intelligent enemy AI
- Epic boss battles
- Beautiful neon cyber aesthetic
- Score & highscore tracking

## Installation

### Requirements
- Python 3.7+
- pygame

### Install Dependencies

```bash
pip install pygame
```

## How to Play

### Start the Game

```bash
cd snake_cool
python main.py
```

### Controls

- **Arrow Keys**: Move snake
- **ESC**: Pause game / Return to menu
- **SPACE**: Restart (when game over)
- **Mouse**: Click menu items

## Game Features

### Food Items
- **Apples** (Red): +10 points, common
- **Bananas** (Gold): +50 points, rare (15% spawn chance)

### Enemies
- Spawn at 50+ score
- Intelligent AI with chase and wander behavior
- Avoid or die!
- Maximum 3 enemies

### Boss Fight
- Spawns at 200 points
- Shoots projectiles at you
- Has 5 health points
- Orbits around you while shooting
- Defeat for +100 bonus points

### Scoring
- Apple: 10 points
- Banana: 50 points
- Boss defeat: 100 points
- New highscore is automatically saved!

## Game Mechanics

### Difficulty Progression
1. **0-49 pts**: Classic Snake
2. **50-199 pts**: Enemies start spawning (1-3 based on score)
3. **200+ pts**: Boss appears with projectile attacks!

### Death Conditions
- Hit wall
- Hit yourself
- Hit enemy
- Get hit by boss projectile

## Visual Features

- **Neon Cyber Theme**: Modern dark background with glowing elements
- **Snake**: Gradient body with glowing head
- **Enemies**: Pulsing red glow, eyes change color when chasing
- **Boss**: Massive 2x2 size with intense multi-layer glow effects
- **Bananas**: Special sparkle effects for rare items
- **Projectiles**: Glowing energy balls

## File Structure

```
snake_cool/
├── main.py          # Entry point
├── game.py          # Main game loop
├── snake.py         # Snake logic
├── enemy.py         # Enemy AI
├── boss.py          # Boss system
├── projectile.py    # Projectile system
├── food.py          # Food spawning
├── ui.py            # UI rendering
├── menu.py          # Menu system
├── constants.py     # Game constants
├── highscore.json   # Saved highscore (auto-generated)
└── README.md        # This file
```

## Technical Details

- **Window Size**: 1200x800 pixels
- **Grid**: 30x20 cells
- **Cell Size**: 40x40 pixels
- **Target FPS**: 60
- **Snake Speed**: 8 moves/second

## Credits

Created during a live demonstration of Claude Code 2 capabilities at **AssistDigital Leipzig**.

**Technologies:**
- Python 3
- Pygame
- Claude Code 2
- Claude Sonnet 4.5

## Tips for High Scores

1. Focus on bananas - they're worth 5x apples!
2. Lead enemies into each other or corners
3. Use the entire screen space
4. During boss fight, keep moving in circles
5. Don't get too long too fast - harder to maneuver!

## Enjoy the Game!

Have fun and try to beat the highscore! 🐍🎮✨
