# Implementierungsplan: Snake Cool Game

## Präsentation Live-Demo
AssistDigital Leipzig - Claude Code 2 & Claude Sonnet 4.5 Demo

---

## 1. Projektübersicht

### Ziel
Ein erweitertes Snake Game in Python mit pygame, das deutlich über das klassische Snake-Gameplay hinausgeht.

### Kern-Features
- Klassisches Snake-Gameplay als Basis
- Intelligente KI-Gegner mit Verfolgungslogik
- Boss-Kampf-System mit Projektilen
- Score & Highscore Tracking
- Item-System (Äpfel, Bananen)
- Professionelles Hauptmenü
- Moderne, kreative Optik

---

## 2. Technische Architektur

### 2.1 Projektstruktur
```
snake_cool/
├── main.py              # Haupteinstiegspunkt
├── game.py              # Hauptspiel-Loop und State Management
├── snake.py             # Snake-Klasse und Logik
├── enemy.py             # Enemy-KI mit Pathfinding
├── boss.py              # Boss-Logik mit Schießmechanik
├── food.py              # Food-Items (Äpfel, Bananen)
├── projectile.py        # Projektil-System für Boss
├── menu.py              # Hauptmenü-System
├── ui.py                # UI-Elemente (Score, Highscore)
├── constants.py         # Globale Konstanten
└── highscore.json       # Persistenter Highscore
```

### 2.2 Technologie-Stack
- **Python 3.x**
- **pygame** für Grafik und Input
- **JSON** für Highscore-Persistierung
- **Algorithmus**: A* oder einfacherer Pathfinding für Gegner-KI

---

## 3. Detaillierte Komponenten-Planung

### 3.1 Constants & Configuration (constants.py)

**Zweck**: Zentrale Konfiguration aller Spielparameter

**Wichtige Konstanten**:
```python
# Display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 40  # Große Zellen für gute Sichtbarkeit
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (Moderne Farbpalette)
BACKGROUND_COLOR = (20, 20, 30)
SNAKE_HEAD_COLOR = (50, 220, 150)
SNAKE_BODY_COLOR = (40, 180, 120)
ENEMY_COLOR = (220, 50, 50)
BOSS_COLOR = (180, 0, 80)
APPLE_COLOR = (220, 20, 60)
BANANA_COLOR = (255, 215, 0)

# Game Balance
SNAKE_SPEED = 10  # FPS-basiert
ENEMY_SPAWN_SCORE = 50
MAX_ENEMIES = 3
BOSS_SPAWN_SCORE = 200
BANANA_SPAWN_CHANCE = 0.15
APPLE_POINTS = 10
BANANA_POINTS = 50
```

---

### 3.2 Snake-Klasse (snake.py)

**Verantwortlichkeiten**:
- Schlangenbewegung und Wachstum
- Kollisionserkennung (Wände, Selbst)
- Richtungssteuerung

**Wichtige Methoden**:
```python
class Snake:
    def __init__(self, start_pos)
    def move(self)
    def grow(self)
    def change_direction(self, new_direction)
    def check_collision_with_self(self)
    def check_collision_with_walls(self)
    def draw(self, surface)
```

**Besonderheiten**:
- Body als Liste von (x, y) Positionen
- Head hat andere Farbe als Body
- Smooth Movement auf Grid-Basis
- Input-Buffering für präzise Steuerung

---

### 3.3 Gegner-KI (enemy.py)

**Ziel**: Interessante Verfolgungslogik, nicht triviales "auf Spieler zurennen"

**KI-Strategie**:
1. **Distanz-Check**: Aktiviert sich nur wenn Spieler in bestimmter Reichweite
2. **Pathfinding-Light**: Vereinfachter A* oder "intelligentes Bewegen"
   - Berechnet optimale Richtung zum Snake-Kopf
   - Vermeidet Snake-Body als Hindernisse
   - Hat "Cooldown" zwischen Richtungsänderungen für natürlicheres Verhalten
3. **Wanderverhalten**: Bei großer Distanz zufällige Bewegung
4. **Vorsicht**: Stoppt oder weicht aus wenn zu nah am Snake-Body

**Klassen-Struktur**:
```python
class Enemy:
    def __init__(self, pos)
    def update(self, snake_head_pos, snake_body)
    def calculate_next_move(self, target_pos, obstacles)
    def wander(self)
    def draw(self, surface)
```

**Parameter**:
- Bewegungsgeschwindigkeit: Langsamer als Snake
- Aktivierungsradius: 15 Zellen
- Richtungswechsel-Cooldown: 0.3 Sekunden

---

### 3.4 Boss-System (boss.py)

**Aktivierung**: Bei Score >= 200

**Boss-Verhalten**:
1. **Spawnt in der Mitte** des Spielfelds
2. **Bewegung**:
   - Bewegt sich langsam
   - Hält Abstand zum Spieler (kein direkter Kontakt)
   - Umkreist den Spieler
3. **Angriff**:
   - Schießt Projektile auf Snake-Kopf
   - Schussfrequenz: Alle 2 Sekunden
   - Projektile haben moderate Geschwindigkeit
4. **Health System**:
   - Boss hat HP (z.B. 5 Treffer)
   - Spieler kann Boss besiegen durch Körper-Kollision (riskant!)
   - Nach Besiegung: Großer Score-Bonus

**Klassen-Struktur**:
```python
class Boss:
    def __init__(self, pos)
    def update(self, snake_head_pos)
    def shoot_projectile(self, target_pos)
    def take_damage(self)
    def is_alive(self)
    def draw(self, surface)
```

---

### 3.5 Projektil-System (projectile.py)

**Zweck**: Boss-Projektile die Snake treffen können

**Eigenschaften**:
```python
class Projectile:
    def __init__(self, start_pos, target_pos, speed)
    def update(self)
    def check_collision(self, snake_segments)
    def is_off_screen(self)
    def draw(self, surface)
```

**Verhalten**:
- Bewegt sich linear in Richtung des Ziels
- Verschwindet bei Bildschirmrand
- Tötet Snake bei Kollision
- Visuelle Effekte: Glühende Kugel oder Laser

---

### 3.6 Food-System (food.py)

**Items**:
1. **Äpfel** (90% Spawn-Chance)
   - +10 Punkte
   - Rote Farbe
   - Snake wächst um 1 Segment

2. **Bananen** (10% Spawn-Chance)
   - +50 Punkte
   - Goldene Farbe
   - Snake wächst um 1 Segment
   - Visueller Highlight-Effekt

**Klassen-Struktur**:
```python
class Food:
    def __init__(self, food_type='apple')
    def spawn(self, occupied_cells)
    def get_points(self)
    def draw(self, surface)
```

**Spawn-Logik**:
- Niemals auf Snake oder Gegnern spawnen
- Zufällige Position auf Grid
- Nach Aufnahme: Neues Item spawnt sofort

---

### 3.7 UI-System (ui.py)

**Verantwortlichkeiten**:
- Score-Anzeige (aktuell)
- Highscore-Anzeige
- Boss-Health-Bar
- Game-Over Screen

**Komponenten**:
```python
class UI:
    def draw_score(self, surface, score)
    def draw_highscore(self, surface, highscore)
    def draw_boss_health(self, surface, boss_hp, max_hp)
    def draw_game_over(self, surface, final_score)
```

**Design**:
- Moderne Sans-Serif Schrift
- Großer, gut lesbarer Text
- Positionierung: Oben links (Score), Oben rechts (Highscore)
- Farbschema passend zum Spiel

---

### 3.8 Hauptmenü (menu.py)

**Screens**:
1. **Main Menu**
   - Titel: "SNAKE COOL"
   - Buttons: "Start Game", "Quit"
   - Highscore-Anzeige
2. **Pause Menu** (ESC während Spiel)
   - "Resume"
   - "Main Menu"
   - "Quit"

**Klassen-Struktur**:
```python
class Menu:
    def __init__(self)
    def draw_main_menu(self, surface, highscore)
    def draw_pause_menu(self, surface)
    def handle_input(self, event)
    def get_selected_option(self)
```

**Interaktion**:
- Maus-Hover-Effekte
- Click-Feedback
- Tastatur-Navigation (Pfeiltasten + Enter)

---

### 3.9 Game State Manager (game.py)

**States**:
- `MENU` - Hauptmenü
- `PLAYING` - Aktives Spiel
- `PAUSED` - Pause-Menü
- `GAME_OVER` - Game Over Screen

**Hauptklasse**:
```python
class Game:
    def __init__(self)
    def run(self)
    def handle_events(self)
    def update(self)
    def draw(self)
    def reset_game(self)
    def load_highscore(self)
    def save_highscore(self)
```

**Game Loop**:
```python
while running:
    # 1. Event Handling
    handle_events()

    # 2. Update Game State
    if state == PLAYING:
        update_snake()
        update_enemies()
        update_boss()
        update_projectiles()
        check_collisions()
        spawn_enemies()
        spawn_boss()

    # 3. Render
    draw_background()
    draw_food()
    draw_snake()
    draw_enemies()
    draw_boss()
    draw_projectiles()
    draw_ui()

    # 4. Frame Rate
    clock.tick(60)
```

---

## 4. Implementierungs-Reihenfolge

### Phase 1: Grundgerüst (30 Minuten)
1. ✅ `constants.py` - Alle Konstanten definieren
2. ✅ `main.py` - Pygame Initialisierung
3. ✅ `snake.py` - Basis Snake-Klasse mit Bewegung
4. ✅ `food.py` - Food-Spawning
5. ✅ `game.py` - Grundlegender Game Loop

**Testmeilenstein**: Spielbares klassisches Snake

---

### Phase 2: UI & Menu (20 Minuten)
6. ✅ `ui.py` - Score/Highscore Anzeige
7. ✅ `menu.py` - Hauptmenü und Pause-Menü
8. ✅ Highscore-Persistierung (JSON)

**Testmeilenstein**: Vollständiges Menü-System

---

### Phase 3: Gegner-System (30 Minuten)
9. ✅ `enemy.py` - Enemy-Klasse mit Basic AI
10. ✅ Enemy-Spawning-Logik
11. ✅ Kollisionserkennung Snake <-> Enemy
12. ✅ Intelligente Pathfinding-Verbesserung

**Testmeilenstein**: Funktionierende Gegner mit interessanter KI

---

### Phase 4: Boss-System (40 Minuten)
13. ✅ `projectile.py` - Projektil-Klasse
14. ✅ `boss.py` - Boss-Klasse mit Movement
15. ✅ Boss-Schussmechanik
16. ✅ Boss-Health und Defeat-Logik
17. ✅ Boss-UI Integration

**Testmeilenstein**: Vollständiger Boss-Fight

---

### Phase 5: Polish & Visuals (30 Minuten)
18. ✅ Kreative visuelle Verbesserungen
    - Partikel-Effekte für Essen
    - Glühen für seltene Items
    - Animations-Tweening
    - Screen-Shake bei Boss-Spawn
19. ✅ Sound-Effekte (optional, wenn Zeit)
20. ✅ Feintuning Game-Balance
21. ✅ Bug-Fixing

**Testmeilenstein**: Poliertes, präsentationsfähiges Spiel

---

## 5. Besondere Design-Entscheidungen

### 5.1 Kreative Optik - Ideen

**Farbschema**: Neon-Cyber-Look
- Dunkler Hintergrund (fast schwarz)
- Leuchtende Neon-Farben für Game-Objekte
- Glüheffekte (glow) für wichtige Elemente

**Visuelle Details**:
1. **Snake**:
   - Gradient von hell (Kopf) zu dunkel (Ende)
   - Subtile Animation/Pulsierung
2. **Enemies**:
   - Rötliches Glühen
   - "Radar-Ping" Animation wenn sie aktivieren
3. **Boss**:
   - Größer als normale Enemies
   - Intensive Glow-Effekte
   - Screen Shake bei Spawn
4. **Food**:
   - Rotation/Pulsierung
   - Glitzer-Partikel bei Bananen
5. **Background**:
   - Subtiles Grid-Muster
   - Leichter Gradient

---

### 5.2 Game Balance

**Schwierigkeitskurve**:
- Start: Nur Food sammeln
- Score 50+: Erste Enemies spawnen
- Score 100+: 2 Enemies
- Score 150+: 3 Enemies (Maximum)
- Score 200+: Boss erscheint

**Snake-Geschwindigkeit**:
- Konstant (nicht steigend) für faire Boss-Kämpfe
- Aber: Längerer Snake = schwieriger zu manövrieren

**Boss-Balance**:
- Schüsse sind ausweichbar
- Boss ist langsam
- Belohnung: +100 Punkte bei Defeat

---

## 6. Potenzielle Herausforderungen & Lösungen

### 6.1 Challenge: Enemy Pathfinding Performance
**Problem**: A* kann bei vielen Enemies laggen
**Lösung**:
- Vereinfachter "Greedy Best-First" Ansatz
- Update nur alle N Frames
- Maximum 3 Enemies gleichzeitig

### 6.2 Challenge: Boss-Projektile vs. lange Snake
**Problem**: Snake-Body macht Ausweichen schwer
**Lösung**:
- Projektile treffen nur Head
- Boss hält Abstand
- Langsame Projektile

### 6.3 Challenge: Food-Spawning bei vollem Bildschirm
**Problem**: Bei langer Snake wenig Platz
**Lösung**:
- Algorithmus findet freie Zellen
- Notfalls: Zufällige Position (selten)

---

## 7. Testing-Strategie

### Test-Cases:
1. ✅ Snake bewegt sich korrekt in alle Richtungen
2. ✅ Snake wächst beim Essen
3. ✅ Kollision mit Wand = Game Over
4. ✅ Kollision mit sich selbst = Game Over
5. ✅ Enemies spawnen bei richtigem Score
6. ✅ Enemies verfolgen intelligent
7. ✅ Boss spawnt bei Score 200
8. ✅ Boss-Projektile treffen Snake
9. ✅ Highscore wird korrekt gespeichert
10. ✅ Menü-Navigation funktioniert
11. ✅ ESC öffnet Pause-Menü
12. ✅ Banana spawnt selten, gibt mehr Punkte

---

## 8. Erweiterungsmöglichkeiten (Future)

Falls noch Zeit oder für Version 2:
- **Power-Ups**: Speed Boost, Invincibility, Double Points
- **Unterschiedliche Boss-Patterns**: Mehrere Boss-Typen
- **Levels**: Hindernisse, Wände im Spielfeld
- **Multiplayer**: Lokaler 2-Player Modus
- **Achievements**: System für Erfolge
- **Leaderboard**: Online Highscore-Tabelle

---

## 9. Geschätzte Entwicklungszeit

**Gesamt: ~2.5 Stunden für komplette Implementierung**

- Setup & Grundgerüst: 30 Min
- UI & Menu: 20 Min
- Enemy-System: 30 Min
- Boss-System: 40 Min
- Polish & Visuals: 30 Min

---

## 10. Zusammenfassung

Dieses Snake Cool Game wird ein deutliches Upgrade zum klassischen Snake sein:

**Highlights**:
- 🎮 Moderne, großformatige Optik
- 🤖 Intelligente Gegner-KI
- 👾 Epischer Boss-Kampf
- 🍌 Abwechslungsreiches Item-System
- 🏆 Persistentes Highscore-System
- 🎨 Kreative Neon-Cyber-Ästhetik

**Technisch solide**:
- Modulare Code-Struktur
- Saubere Klassen-Hierarchie
- Erweiterbar und wartbar

Bereit für Live-Demo bei AssistDigital Leipzig! 🚀

---

**Nächster Schritt**: Implementierung nach diesem Plan! 🎯
