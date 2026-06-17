from uuid import UUID
from typing import Optional
from dataclasses import asdict

from tennis_match_scoreboard.dtos import MatchScoreDto, PlayerScoreDto, GameDto
from tennis_match_scoreboard.models import Player, Match


class NewMatchService:
    """
    Service class for handling business logic of creating a new match.
    """

    @staticmethod
    def create_match(player1: Player, player2: Player) -> Optional[UUID]:
        player1 = Player.objects.get_or_create(name=player1)[0]
        player2 = Player.objects.get_or_create(name=player2)[0]
        match_score = MatchScoreDto(
            player1=PlayerScoreDto(
                sets=0, won_games=0, current_game=GameDto(points=0, advantage=False)
            ),
            player2=PlayerScoreDto(
                sets=0, won_games=0, current_game=GameDto(points=0, advantage=False)
            ),
            tie_break=False
        )
        match = Match.objects.create(player1=player1, player2=player2, score=asdict(match_score))
        return match.uuid
