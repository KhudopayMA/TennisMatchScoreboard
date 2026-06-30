from unittest.mock import patch
from dataclasses import asdict

import pytest

from tennis_match_scoreboard.dtos import MatchScoreDto, GameDto, PlayerScoreDto
from tennis_match_scoreboard.services import ScoreService
from tennis_match_scoreboard.models import Match, Player


@pytest.fixture
def deuce_match() -> Match:
    match_score = MatchScoreDto(
        player1=PlayerScoreDto(
            sets=0,
            games=0,
            current_game=GameDto(points=40, advantage=False),
        ),
        player2=PlayerScoreDto(
            sets=0,
            games=0,
            current_game=GameDto(points=40, advantage=False),
        ),
        tie_break=False,
    )

    return Match(
        player1=Player(name="first"),
        player2=Player(name="second"),
        score=asdict(match_score),
    )


class TestScoreService:
    def test_add_point_when_deuce(self, deuce_match: Match) -> None:

        with patch(
            "tennis_match_scoreboard.models.Match.objects"
        ) as mock_objects:
            mock_objects.get.return_value = deuce_match

            with patch.object(Match, "save", return_value=None):
                score_service = ScoreService(str(deuce_match.uuid))
                score_service.add_point("first")

                assert (
                    score_service.match_score.player1.current_game.advantage
                    is True
                )
                assert (
                    score_service.match_score.player1.current_game.points == 40
                )
                assert score_service.match.winner is None
