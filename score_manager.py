# Score Management and Persistence
import os
from config import *

class ScoreManager:
    """Manages current score and highscore with file persistence"""

    def __init__(self):
        self.score = 0
        self.highscore = self.load_highscore()
        self.highscore_file = "highscore.txt"

    def add_score(self, points):
        """Add points to current score"""
        self.score += points

        # Update highscore if needed
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()

    def reset(self):
        """Reset current score (for new game)"""
        self.score = 0

    def load_highscore(self):
        """Load highscore from file"""
        try:
            if os.path.exists("highscore.txt"):
                with open("highscore.txt", "r") as f:
                    return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            pass
        return 0

    def save_highscore(self):
        """Save highscore to file"""
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))
        except IOError:
            print("Warning: Could not save highscore")

    def get_score(self):
        """Get current score"""
        return self.score

    def get_highscore(self):
        """Get highscore"""
        return self.highscore

    def should_spawn_boss(self):
        """Check if score is at a boss spawn threshold"""
        if self.score >= BOSS_SPAWN_SCORE and self.score % BOSS_SPAWN_SCORE == 0:
            return True
        return False
