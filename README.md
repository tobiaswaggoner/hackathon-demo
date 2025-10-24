# Snake (pygame) – Minimal

Ein sehr einfaches Snake-Spiel mit `pygame` ohne Schnickschnack.

## Steuerung
- Pfeiltasten oder WASD: Bewegen
- R: Nach Game Over neu starten
- ESC oder Fenster schließen: Beenden

## Voraussetzungen
- Python 3.9+ empfohlen

## Installation
Empfohlen: Virtuelle Umgebung anlegen und Abhängigkeiten installieren.

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Start
```powershell
python main.py
```

## Anpassungen
- Geschwindigkeit: `FPS` in `main.py`
- Spielfeldgröße: `GRID_WIDTH`, `GRID_HEIGHT` und `TILE_SIZE` in `main.py`
