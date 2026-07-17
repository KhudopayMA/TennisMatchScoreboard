from dataclasses import asdict

from django.test import TestCase

from tennis_match_scoreboard.dtos import GameDto, MatchScoreDto, PlayerScoreDto
from tennis_match_scoreboard.models import Match, Player
from tennis_match_scoreboard.services import ScoreService


class TestScoreService(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(name="first")
        self.player2 = Player.objects.create(name="second")

        self.deuce_match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            score = asdict(self._get_deuce_match_score())
        )

        self.player1_next_point_win_game_match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            score=asdict(self._player1_next_point_win_game_match_score())
        )

        self.next_point_starts_tie_break_match = Match.objects.create(
            player1=self.player1,
            player2=self.player2,
            score=asdict(self._next_point_starts_tie_break_match())
        )



    @staticmethod
    def _get_deuce_match_score() -> MatchScoreDto:
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
        return match_score

    @staticmethod
    def _player1_next_point_win_game_match_score() -> MatchScoreDto:
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

        return match_score


    @staticmethod
    def _next_point_starts_tie_break_match() -> MatchScoreDto:
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

        return match_score

    def test_add_point_when_deuce(self) -> None:
        """ Test add a point to the match in a deuce state """
        score_service = ScoreService(self.deuce_match)
        score_service.add_point(self.player1.name)

        assert (
                score_service.match_score.player1.current_game.advantage
                is True
        )
        assert (
                score_service.match_score.player1.current_game.points == 40
        )
        assert score_service.match.winner is None

    def test_add_point_player1_win_game(self) -> None:
        """ Test a player1 win the game when a point is added """

        score_service = ScoreService(self.player1_next_point_win_game_match)
        score_service.add_point("first")

        assert score_service.match_score.player1.games > 0
        assert (
                score_service.match_score.player1.current_game.points == 0
        )

    def test_tie_break_starts(self) -> None:
        """ Test tie_break starts when a point is added to a player1  """

        score_service = ScoreService(self.next_point_starts_tie_break_match)
        score_service.add_point("first")

        assert score_service.match_score.tie_break is True
