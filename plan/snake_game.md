# Snake Game - Detaillierter Implementierungsplan

## Projekt-Übersicht
Ein erweitertes Snake Game in Python mit pygame, das klassische Gameplay mit modernen Game-Mechaniken kombiniert.

## Technische Spezifikationen

### Grundlegende Anforderungen
- **Sprache**: Python 3.x
- **Framework**: pygame
- **Fenstergröße**: 1200x800 Pixel (relativ groß wie gewünscht)
- **Ziel-FPS**: 60 FPS für flüssiges Gameplay

### Dateistruktur
```
hackathon_demo/
├── snake_game.py           # Hauptdatei mit Game Loop
├── game_objects.py         # Snake, Enemy, Boss, Food Klassen
├── ai_behavior.py          # AI-Logik für Gegner
├── score_manager.py        # Score und Highscore Verwaltung
├── config.py               # Konstanten und Konfiguration
└── assets/                 # Optional: Sounds, Bilder
```

## Phase 1: Basis-Spielmechanik

### 1.1 Snake Klasse
**Eigenschaften:**
- Position (Liste von Segmenten)
- Bewegungsrichtung
- Geschwindigkeit
- Wachstums-Counter

**Methoden:**
- `move()` - Bewegung basierend auf Richtung
- `grow()` - Schlange verlängern
- `check_collision()` - Kollision mit Wand/sich selbst
- `draw()` - Rendering

**Design-Entscheidungen:**
- Segment-basierte Darstellung (Rechtecke)
- Gitter-basierte Bewegung (Grid-System 20x20 Pixel pro Zelle)
- Head-Segment hat andere Farbe als Body

### 1.2 Food System
**Eigenschaften:**
- Zufällige Position (auf Grid)
- Verschiedene Typen (normal, bonus)

**Mechanik:**
- Normales Food: +1 Segment, +10 Score
- Bonus Food (selten): +3 Segmente, +50 Score
- Spawn-Rate: 5% Chance für Bonus Food

### 1.3 Spielfeld & Kollision
- Spielfeld: 60x40 Zellen (1200x800 / 20 = 60x40)
- Wände töten die Schlange
- Selbst-Kollision beendet das Spiel
- Kollisionsbox pro Segment

## Phase 2: Score & Highscore System

### 2.1 Score Manager
**Funktionen:**
- Aktuellen Score tracken
- Highscore in Datei speichern (`highscore.txt`)
- Score-Multiplikator für Combos
- Punkteverteilung:
  - Normales Food: 10 Punkte
  - Bonus Food: 50 Punkte
  - Gegner besiegt: 100 Punkte
  - Boss besiegt: 500 Punkte

### 2.2 UI Elemente
**Anzeige:**
- Aktueller Score: Top-left (großer Font)
- Highscore: Top-right (mittlerer Font)
- Level/Welle: Top-center
- Leben/Health bar (falls implementiert)

**Font & Style:**
- pygame.font für saubere Darstellung
- Kontrastreiche Farben (Weiß auf dunklem Hintergrund)

## Phase 3: Intelligente Gegner-AI

### 3.1 Enemy Klasse
**Eigenschaften:**
- Position
- Geschwindigkeit (langsamer als Snake)
- Gesundheit (3 Hits zum Töten)
- AI-State (Patrol, Chase, Evade)

### 3.2 AI-Verhalten (Interessante Mechanik!)
**State Machine:**

1. **Patrol Mode** (Standard):
   - Bewegt sich in zufälligen Richtungen
   - Wechselt alle 2-3 Sekunden die Richtung
   - Bleibt in bestimmtem Radius vom Spawn-Punkt

2. **Chase Mode** (wenn Snake in Range):
   - Aktiviert wenn Snake < 300 Pixel entfernt
   - Nutzt A*-ähnlichen Pfadfindungs-Algorithmus
   - ABER: Macht absichtliche "Fehler" für Interessantheit:
     - 20% Chance pro Frame die falsche Richtung zu wählen
     - Verzögerung in Reaktionszeit (0.3 Sekunden)
     - Wird langsamer wenn sehr nah (< 50 Pixel)

3. **Evade Mode** (wenn Snake sehr lang):
   - Aktiviert wenn Snake > 15 Segmente
   - Hält Distanz, greift nicht direkt an
   - Schießt gelegentlich Projektile (alle 3 Sekunden)

**Pathfinding-Vereinfachung:**
- Kein vollständiges A*, sondern vereinfachte Heuristik:
  1. Berechne Vektor zum Ziel
  2. Wähle Richtung die diesem Vektor am nächsten kommt
  3. Prüfe ob Richtung frei ist
  4. Falls blockiert, wähle alternative Richtung
  5. Füge "Fehler" hinzu für unperfektes Verhalten

### 3.3 Enemy Spawning
**Spawn-System:**
- Welle 1: 1 Gegner nach 10 Sekunden
- Welle 2: 2 Gegner nach weiteren 20 Sekunden
- Welle 3+: +1 Gegner pro Welle
- Max. 5 Gegner gleichzeitig auf dem Feld

**Spawn-Locations:**
- Immer an Rand des Spielfelds
- Mindestens 300 Pixel von Snake entfernt
- Nicht innerhalb von 100 Pixel von anderem Gegner

## Phase 4: Boss-Mechanik

### 4.1 Boss Spawn Bedingung
**Trigger:**
- Score erreicht 500 Punkte
- Alle normalen Gegner werden entfernt
- Boss spawnt in Mitte des Bildschirms
- Dramatische Ankündigung ("BOSS APPEARS!")

### 4.2 Boss Eigenschaften
**Stats:**
- Größe: 5x5 Segmente (100x100 Pixel)
- Gesundheit: 20 HP
- Bewegungsgeschwindigkeit: Langsam (30% von Snake)
- Schuss-Rate: Alle 1.5 Sekunden
- Kann nicht von Snake gefressen werden

**Bewegungsmuster:**
- Bewegt sich in wellenartigen Mustern
- Versucht mittlere Distanz zur Snake zu halten (200-400 Pixel)
- Weicht aus wenn Snake zu nah kommt (< 150 Pixel)
- Nutzt Sinuswellen-Bewegung für interessantes Pattern

### 4.3 Schuss-System
**Projektile:**
- Boss schießt in Richtung Snake
- Projektilgeschwindigkeit: Mittel (schneller als Boss, langsamer als Snake)
- 3 Projektile pro Schuss in leichtem Spread-Pattern (0°, -15°, +15°)
- Projektil tötet Snake bei Treffer (oder -1 Leben falls Leben-System)

**Visuals:**
- Rote leuchtende Kugeln
- Trail-Effekt für Bewegung
- Partikel bei Aufprall

### 4.4 Boss Defeat
**Bei Sieg:**
- +500 Score
- Alle Projektile verschwinden
- Victory Screen (3 Sekunden)
- Game continues mit erhöhter Schwierigkeit
- Nächster Boss bei Score +500 (1000, 1500, etc.)

## Phase 5: UI & Polishing

### 5.1 Game States
- **MENU**: Start Screen mit Highscore
- **PLAYING**: Aktives Gameplay
- **PAUSED**: Pause Menü (ESC)
- **GAME_OVER**: End Screen mit Final Score
- **BOSS_INTRO**: Boss Ankündigung

### 5.2 Visual Polish
**Farb-Schema:**
- Hintergrund: Dunkelgrau (#1a1a1a)
- Snake Head: Neon Grün (#00ff00)
- Snake Body: Grün (#00aa00)
- Food: Rot (#ff0000)
- Bonus Food: Gold (#ffd700)
- Enemy: Orange (#ff6600)
- Boss: Dunkelrot (#8b0000)
- Projektile: Hellrot (#ff3333)

**Effekte:**
- Fade-in bei Food spawn
- Screen shake bei Boss spawn
- Partikel bei Food consumption
- Flash bei Hit

### 5.3 Sound Effects (Optional)
- Essen von Food: "munch"
- Snake stirbt: "game over"
- Boss spawnt: dramatische Musik
- Schuss: "pew pew"

## Phase 6: Controls & Input

### Steuerung
**Keyboard:**
- Arrow Keys / WASD: Bewegung
- ESC: Pause
- SPACE: Restart (bei Game Over)
- Q: Quit

**Mechanik:**
- Input buffering für responsive Controls
- Kann nicht direkt um 180° drehen
- Geschwindigkeit konstant (Grid-based movement)

## Implementierungs-Reihenfolge

### Sprint 1: Fundament (30-40 Minuten)
1. Projekt-Setup, pygame initialisieren
2. Snake Klasse + Basic Movement
3. Food System
4. Kollisions-Erkennung
5. Game Loop & Basic UI

### Sprint 2: Score & Enemies (20-30 Minuten)
6. Score Manager + Highscore Persistierung
7. UI für Score/Highscore
8. Enemy Klasse mit Basis-Bewegung
9. Enemy AI States
10. Enemy Spawning System

### Sprint 3: Boss Fight (20-30 Minuten)
11. Boss Klasse
12. Projektil System
13. Boss AI & Movement Patterns
14. Boss Spawn Trigger
15. Victory/Defeat Handling

### Sprint 4: Polish (15-20 Minuten)
16. Game States (Menu, Pause, Game Over)
17. Visual Effects
18. Balancing & Testing
19. Bug Fixes

## Testing Checkpoints

### Checkpoint 1: Basic Gameplay
- Snake bewegt sich korrekt
- Food spawnt und kann gegessen werden
- Kollision funktioniert
- Score erhöht sich

### Checkpoint 2: Enemy AI
- Enemies spawnen korrekt
- AI verhält sich interessant (nicht zu einfach)
- Kollision Snake-Enemy funktioniert
- Pathfinding arbeitet ohne Freeze

### Checkpoint 3: Boss Fight
- Boss spawnt bei richtigem Score
- Schüsse funktionieren
- Boss ist besiegt-bar aber challenging
- Victory Flow funktioniert

### Checkpoint 4: Complete Experience
- Highscore speichert korrekt
- Alle Game States funktionieren
- Keine crashes
- Spielgefühl ist gut

## Technische Herausforderungen & Lösungen

### Challenge 1: AI Pathfinding Performance
**Problem:** A* könnte bei vielen Enemies laggen
**Lösung:** Vereinfachte Heuristik + Update nur alle 0.1s statt jeden Frame

### Challenge 2: Boss Projektil Collision
**Problem:** Präzise Kollision zwischen kleinen Projektilen und Snake
**Lösung:** Radius-based collision mit pygame.math.Vector2.distance()

### Challenge 3: Game Feel
**Problem:** Grid-based Movement kann sich steif anfühlen
**Lösung:** Smooth interpolation zwischen Grid-Positionen für Rendering

### Challenge 4: Balancing
**Problem:** Boss könnte zu einfach/schwer sein
**Lösung:** Konfigurierbare Werte in config.py für schnelles Tuning

## Erweiterungsmöglichkeiten (Future)

- Power-Ups (Speed, Shield, Double Points)
- Multiple Boss-Types
- Procedural Level Generation mit Hindernissen
- Online Leaderboard
- Verschiedene Schwierigkeits-Modi
- Achievements System

## Schätzung

**Gesamt-Implementierungszeit:** 1.5 - 2 Stunden für vollständiges Spiel
**Lines of Code:** ~800-1000 Zeilen
**Dateien:** 5-6 Python Files

---

**Nächster Schritt:** Implementierung gemäß obiger Phasen-Struktur mit config.py beginnend, dann game_objects.py, dann Hauptlogik in snake_game.py
