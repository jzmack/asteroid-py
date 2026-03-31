import pygame
from pathlib import Path

from constants import HIGH_SCORE_FILE, SCORE_COLOR, SCORE_FONT_SIZE, SCORE_POSITION


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.high_score_path = Path(HIGH_SCORE_FILE)
        self.high_score = self._load_high_score()
        self.font = pygame.font.SysFont(None, SCORE_FONT_SIZE)
        self.color = SCORE_COLOR
        self.position = pygame.Vector2(SCORE_POSITION)

    def _load_high_score(self):
        try:
            if not self.high_score_path.exists():
                return 0

            with self.high_score_path.open("r", encoding="utf-8") as high_score_file:
                raw_value = high_score_file.readline().strip()
                return int(raw_value) if raw_value else 0
        except (OSError, ValueError):
            return 0

    def save_high_score(self):
        try:
            self.high_score_path.write_text(str(self.high_score), encoding="utf-8")
        except OSError:
            pass

    def add(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self):
        self.score = 0

    def draw(self, screen):
        score_text = f"SCORE: {self.score}"
        high_text = f"HIGH: {self.high_score}"

        score_surface = self.font.render(score_text, True, self.color)
        high_surface = self.font.render(high_text, True, self.color)

        screen.blit(score_surface, self.position)

        high_position = pygame.Vector2(
            self.position.x,
            self.position.y + score_surface.get_height() + 8,
        )
        screen.blit(high_surface, high_position)
