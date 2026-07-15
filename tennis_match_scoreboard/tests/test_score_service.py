from dataclasses import asdict
from unittest.mock import patch

import pytest

from tennis_match_scoreboard.dtos import GameDto, MatchScoreDto, PlayerScoreDto
from tennis_match_scoreboard.models import Match, Player
from tennis_match_scoreboard.services import ScoreService


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


@pytest.fixture
def player1_next_point_win_game_match() -> Match:
    match_score = MatchScoreDto(
        player1=PlayerScoreDto(
            sets=0,
            games=0,
            current_game=GameDto(points=30, advantage=False),
        ),
        player2=PlayerScoreDto(
            sets=0,
            games=0,
            current_game=GameDto(points=0, advantage=False),
        ),
        tie_break=False,
    )

    return Match(
        player1=Player(name="first"),
        player2=Player(name="second"),
        score=asdict(match_score),
    )


@pytest.fixture
def next_point_starts_tie_break_match() -> Match:
    match_score = MatchScoreDto(
        player1=PlayerScoreDto(
            sets=0,
            games=5,
            current_game=GameDto(points=30, advantage=False),
        ),
        player2=PlayerScoreDto(
            sets=0,
            games=6,
            current_game=GameDto(points=0, advantage=False),
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

    def test_add_point_player_win_game(
        self, player1_next_point_win_game_match: Match
    ) -> None:

        with patch(
            "tennis_match_scoreboard.models.Match.objects"
        ) as mock_objects:
            mock_objects.get.return_value = player1_next_point_win_game_match

            with patch.object(Match, "save", return_value=None):
                score_service = ScoreService(
                    str(player1_next_point_win_game_match.uuid)
                )
                score_service.add_point("first")

                assert score_service.match_score.player1.games > 0
                assert (
                    score_service.match_score.player1.current_game.points == 0
                )

    def test_tie_break_starts(
        self, next_point_starts_tie_break_match: Match
    ) -> None:

        with patch(
            "tennis_match_scoreboard.models.Match.objects"
        ) as mock_objects:
            mock_objects.get.return_value = next_point_starts_tie_break_match

            with patch.object(Match, "save", return_value=None):
                score_service = ScoreService(
                    str(next_point_starts_tie_break_match.uuid)
                )
                score_service.add_point("first")

                assert score_service.match_score.tie_break is True
