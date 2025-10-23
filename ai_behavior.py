# AI Behavior for Enemies and Boss
import math
import random
from config import *

def update_enemy_ai(enemy, dt, snake, enemies):
    """
    Update enemy AI with state machine: PATROL, CHASE, EVADE
    This is the interesting part - AI that makes intentional 'mistakes' for gameplay!
    """

    snake_head_x, snake_head_y = snake.get_head_pos()
    distance_to_snake = math.sqrt((enemy.x - snake_head_x)**2 + (enemy.y - snake_head_y)**2)

    # Update timers
    enemy.patrol_timer += dt
    enemy.shoot_timer += dt
    enemy.ai_decision_timer += dt

    # Determine state based on distance and snake size
    if len(snake.segments) > ENEMY_EVADE_THRESHOLD:
        enemy.state = "EVADE"
    elif distance_to_snake < ENEMY_DETECTION_RANGE:
        enemy.state = "CHASE"
    else:
        enemy.state = "PATROL"

    # Execute behavior based on state
    if enemy.state == "PATROL":
        _patrol_behavior(enemy, dt)
    elif enemy.state == "CHASE":
        _chase_behavior(enemy, dt, snake_head_x, snake_head_y, distance_to_snake)
    elif enemy.state == "EVADE":
        _evade_behavior(enemy, dt, snake_head_x, snake_head_y)


def _patrol_behavior(enemy, dt):
    """Random wandering around spawn point"""
    # Change direction every 2-3 seconds
    if enemy.patrol_timer > random.uniform(2.0, 3.0):
        enemy.direction = random.uniform(0, 360)
        enemy.patrol_timer = 0

    # Move in current direction
    enemy.x += math.cos(math.radians(enemy.direction)) * enemy.speed * dt
    enemy.y += math.sin(math.radians(enemy.direction)) * enemy.speed * dt

    # Stay within patrol radius (300 pixels from spawn)
    dx = enemy.x - enemy.spawn_x
    dy = enemy.y - enemy.spawn_y
    distance_from_spawn = math.sqrt(dx**2 + dy**2)

    if distance_from_spawn > 300:
        # Turn back toward spawn
        enemy.direction = math.degrees(math.atan2(enemy.spawn_y - enemy.y,
                                                   enemy.spawn_x - enemy.x))

    # Bounce off walls
    _bounce_off_walls(enemy)


def _chase_behavior(enemy, dt, target_x, target_y, distance):
    """Chase the snake with intentional imperfection"""

    # Only update decision every AI_DELAY seconds (reaction time)
    if enemy.ai_decision_timer > ENEMY_AI_DELAY:
        enemy.ai_decision_timer = 0

        # Calculate direction to target
        dx = target_x - enemy.x
        dy = target_y - enemy.y
        perfect_direction = math.degrees(math.atan2(dy, dx))

        # Add intentional error for interesting gameplay
        if random.random() < ENEMY_AI_ERROR_CHANCE:
            # Make a "mistake" - add random offset
            error = random.uniform(-90, 90)
            enemy.direction = perfect_direction + error
        else:
            enemy.direction = perfect_direction

    # Slow down when very close (makes it easier to dodge)
    speed_multiplier = 1.0
    if distance < ENEMY_CLOSE_RANGE:
        speed_multiplier = 0.5

    # Move toward target
    enemy.x += math.cos(math.radians(enemy.direction)) * enemy.speed * speed_multiplier * dt
    enemy.y += math.sin(math.radians(enemy.direction)) * enemy.speed * speed_multiplier * dt

    # Bounce off walls
    _bounce_off_walls(enemy)


def _evade_behavior(enemy, dt, target_x, target_y):
    """Keep distance and shoot projectiles"""

    # Move away from snake
    dx = enemy.x - target_x
    dy = enemy.y - target_y
    distance = math.sqrt(dx**2 + dy**2)

    if distance > 0:
        # Normalize and move away
        enemy.direction = math.degrees(math.atan2(dy, dx))
        enemy.x += math.cos(math.radians(enemy.direction)) * enemy.speed * dt
        enemy.y += math.sin(math.radians(enemy.direction)) * enemy.speed * dt

    # Bounce off walls
    _bounce_off_walls(enemy)


def _bounce_off_walls(enemy):
    """Keep enemy inside game bounds"""
    margin = GRID_SIZE

    if enemy.x < margin:
        enemy.x = margin
        enemy.direction = 180 - enemy.direction
    elif enemy.x > WINDOW_WIDTH - margin:
        enemy.x = WINDOW_WIDTH - margin
        enemy.direction = 180 - enemy.direction

    if enemy.y < margin:
        enemy.y = margin
        enemy.direction = -enemy.direction
    elif enemy.y > WINDOW_HEIGHT - margin:
        enemy.y = WINDOW_HEIGHT - margin
        enemy.direction = -enemy.direction


def update_boss_ai(boss, dt, snake):
    """
    Boss AI: Maintains medium distance, moves in wave pattern, shoots regularly
    """

    snake_head_x, snake_head_y = snake.get_head_pos()
    dx = snake_head_x - boss.x
    dy = snake_head_y - boss.y
    distance = math.sqrt(dx**2 + dy**2)

    # Update wave offset for sinusoidal movement
    boss.wave_offset += dt * 2

    # Determine desired movement based on distance
    if distance < BOSS_MIN_DISTANCE:
        # Too close - move away
        angle = math.degrees(math.atan2(-dy, -dx))
    elif distance > BOSS_MAX_DISTANCE:
        # Too far - move closer
        angle = math.degrees(math.atan2(dy, dx))
    else:
        # Good distance - circle around with wave pattern
        angle = math.degrees(math.atan2(dy, dx)) + 90

    # Add sinusoidal wave to movement for interesting pattern
    wave_amplitude = 50
    perpendicular_angle = angle + 90
    wave_x = math.cos(math.radians(perpendicular_angle)) * math.sin(boss.wave_offset) * wave_amplitude * dt
    wave_y = math.sin(math.radians(perpendicular_angle)) * math.sin(boss.wave_offset) * wave_amplitude * dt

    # Apply movement
    boss.x += math.cos(math.radians(angle)) * boss.speed * dt + wave_x
    boss.y += math.sin(math.radians(angle)) * boss.speed * dt + wave_y

    # Keep boss on screen (with margin)
    margin = BOSS_SIZE * GRID_SIZE // 2 + 20
    boss.x = max(margin, min(WINDOW_WIDTH - margin, boss.x))
    boss.y = max(margin, min(WINDOW_HEIGHT - margin, boss.y))

    # Update shoot timer
    boss.shoot_timer += dt


def should_enemy_shoot(enemy):
    """Check if enemy should shoot (only in EVADE mode)"""
    if enemy.state == "EVADE" and enemy.shoot_timer >= ENEMY_SHOOT_COOLDOWN:
        enemy.shoot_timer = 0
        return True
    return False


def should_boss_shoot(boss):
    """Check if boss should shoot"""
    if boss.shoot_timer >= BOSS_SHOOT_COOLDOWN:
        boss.shoot_timer = 0
        return True
    return False


def get_enemy_shoot_angle(enemy, snake):
    """Calculate angle to shoot at snake"""
    snake_x, snake_y = snake.get_head_pos()
    dx = snake_x - enemy.x
    dy = snake_y - enemy.y
    return math.degrees(math.atan2(dy, dx))


def get_boss_shoot_angles(boss, snake):
    """Calculate angles for boss 3-way spread shot"""
    snake_x, snake_y = snake.get_head_pos()
    dx = snake_x - boss.x
    dy = snake_y - boss.y
    base_angle = math.degrees(math.atan2(dy, dx))

    # Return 3 angles with spread
    return [
        base_angle - BOSS_PROJECTILE_SPREAD,
        base_angle,
        base_angle + BOSS_PROJECTILE_SPREAD
    ]
