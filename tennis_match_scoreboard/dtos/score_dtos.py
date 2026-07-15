from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class GameDto:
    points: int
    advantage: bool


@dataclass(slots=True, kw_only=True)
class PlayerScoreDto:
    current_game: GameDto
    games: int
    sets: int


@dataclass(slots=True, kw_only=True)
class MatchScoreDto:
    player1: PlayerScoreDto
    player2: PlayerScoreDto
    tie_break: bool
