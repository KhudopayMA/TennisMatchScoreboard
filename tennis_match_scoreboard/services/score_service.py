from dataclasses import asdict

from bidict import bidict

from tennis_match_scoreboard.dtos import GameDto, MatchScoreDto, PlayerScoreDto
from tennis_match_scoreboard.models import Match


class ScoreService:
    """
    Service class for handling business logic of the score.
    """

    TENNIS_POINTS: bidict[int, int] = bidict({0: 0, 1: 15, 2: 30, 3: 40})

    def __init__(self, match: Match) -> None:
        self.match = match
        self.match_score = MatchScoreDto(
            player1=PlayerScoreDto(
                sets=self.match.score["player1"]["sets"],
                games=self.match.score["player1"]["games"],
                current_game=GameDto(
                    **self.match.score["player1"]["current_game"]
                ),
            ),
            player2=PlayerScoreDto(
                sets=self.match.score["player2"]["sets"],
                games=self.match.score["player2"]["games"],
                current_game=GameDto(
                    **self.match.score["player2"]["current_game"]
                ),
            ),
            tie_break=self.match.score["tie_break"],
        )

    def add_point(self, player_name: str) -> None:
        point_winner, point_loser = self._resolve_players(player_name)
        if self.match_score.tie_break:
            self._add_tie_break_point(point_winner, point_loser)
        else:
            self._add_standard_point(point_winner, point_loser)
        self.match.score = asdict(self.match_score)
        self.match.save()

    def _resolve_players(
        self, player_name: str
    ) -> tuple[PlayerScoreDto, PlayerScoreDto]:
        if self.match.player1.name == player_name:
            return self.match_score.player1, self.match_score.player2
        else:
            return self.match_score.player2, self.match_score.player1

    def _add_standard_point(
        self, point_winner: PlayerScoreDto, point_loser: PlayerScoreDto
    ) -> None:
        """
        Implements logic of adding standard points.
        """
        if point_winner.current_game.advantage:
            self._add_game(point_winner, point_loser)
        elif point_loser.current_game.advantage:
            point_loser.current_game.advantage = False
        elif (
            point_winner.current_game.points == 40
            and point_loser.current_game.points == 40
        ):
            point_winner.current_game.advantage = True
        else:
            point_winner.current_game.points = self.TENNIS_POINTS[
                self.TENNIS_POINTS.inverse[point_winner.current_game.points]
                + 1
            ]
            if point_winner.current_game.points == 40 and (
                self.TENNIS_POINTS.inverse[point_winner.current_game.points]
                - self.TENNIS_POINTS.inverse[point_loser.current_game.points]
                >= 2
            ):
                self._add_game(point_winner, point_loser)

    def _add_game(
        self, point_winner: PlayerScoreDto, point_loser: PlayerScoreDto
    ) -> None:
        self._reset_game()
        point_winner.games += 1
        if point_winner.games == 6 and point_loser.games == 6:
            self.match_score.tie_break = True
        elif point_winner.games >= 6 and (
            point_winner.games - point_loser.games >= 2
        ):
            self._add_set(point_winner)

    def _add_set(self, point_winner: PlayerScoreDto) -> None:
        self._reset_set()
        point_winner.sets += 1
        if point_winner.sets >= 2:
            self.match.winner = (
                self.match.player1
                if point_winner is self.match_score.player1
                else self.match.player2
            )

    def _reset_game(self) -> None:
        self.match_score.player1.current_game.points = 0
        self.match_score.player2.current_game.points = 0

        self.match_score.player1.current_game.advantage = False
        self.match_score.player2.current_game.advantage = False

    def _reset_set(self) -> None:
        self.match_score.player1.games = 0
        self.match_score.player2.games = 0

    def _add_tie_break_point(
        self, point_winner: PlayerScoreDto, point_loser: PlayerScoreDto
    ) -> None:
        """
        Implements logic of tie-break.
        """
        point_winner.current_game.points += 1
        if (
            point_winner.current_game.points >= 7
            and (
                point_winner.current_game.points
                - point_loser.current_game.points
            )
            >= 2
        ):
            self._add_set(point_winner)
