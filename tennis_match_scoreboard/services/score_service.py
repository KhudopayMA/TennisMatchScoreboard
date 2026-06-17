from dataclasses import asdict

from bidict import bidict

from tennis_match_scoreboard.dtos import MatchScoreDto, PlayerScoreDto, GameDto
from tennis_match_scoreboard.models import Match


class ScoreService:
    """
    Service class for handling business logic of the score.
    """
    TENNIS_POINTS: bidict = bidict(
        {
            0: 0,
            1: 15,
            2: 30,
            3: 40
        }
    )

    def __init__(self, match_uuid):
        self.match = Match.objects.get(uuid=match_uuid)
        self.match_score = MatchScoreDto(
            player1=PlayerScoreDto(
                sets=self.match.score["player1"]["sets"],
                won_games=self.match.score["player1"]["won_games"],
                current_game=GameDto(**self.match.score["player1"]["current_game"])
            ),
            player2=PlayerScoreDto(
                sets=self.match.score["player2"]["sets"],
                won_games=self.match.score["player2"]["won_games"],
                current_game=GameDto(**self.match.score["player2"]["current_game"])
            ),
            tie_break=self.match.score["tie_break"]
        )

    def add_point(self, player_name: str):
        if self.match.player1.name == player_name:
            self.__add_standard_point(1)
        elif self.match.player2.name == player_name:
            self.__add_standard_point(2)
        self.match.score = asdict(self.match_score)
        self.match.save()

    def __add_standard_point(self, player_number: int):
        if self.match_score.tie_break:
            self.__add_tie_break_point(player_number)
        else:
            if player_number == 1:
                if self.match_score.player1.current_game.advantage:
                    self.__reset_game(self.match_score.player1.current_game)
                    self.__add_game(player_number)
                elif self.match_score.player2.current_game.advantage:
                    self.match_score.player2.current_game.advantage = False
                    return
                elif (
                        self.match_score.player1.current_game.points == 40
                        and self.match_score.player2.current_game.points == 40
                ):
                    self.match_score.player1.current_game.advantage = True
                    return
                elif self.match_score.player1.current_game.points == 40:
                    self.__reset_game(self.match_score.player1.current_game)
                    self.__add_game(player_number)
                else:
                    self.match_score.player1.current_game.points = (
                            self.TENNIS_POINTS[
                                self.TENNIS_POINTS.inverse[self.match_score.player1.current_game.points] + 1
                            ]
                    )
                    if (
                            self.match_score.player1.current_game.points - self.match_score.player2.current_game.points
                    ) == 2:
                        self.match_score.player1.won_games += 1
            elif player_number == 2:
                if self.match_score.player2.current_game.advantage:
                    self.__reset_game(self.match_score.player2.current_game)
                    self.__add_game(player_number)
                elif self.match_score.player1.current_game.advantage:
                    self.match_score.player1.current_game.advantage = False
                    return
                elif (
                        self.match_score.player1.current_game.points == 40
                        and self.match_score.player2.current_game.points == 40
                ):
                    self.match_score.player2.current_game.advantage = True
                    return
                elif self.match_score.player2.current_game.points == 40:
                    self.__reset_game(self.match_score.player1.current_game)
                    self.__add_game(player_number)
                else:
                    self.match_score.player2.current_game.points = (
                        self.TENNIS_POINTS[
                            self.TENNIS_POINTS.inverse[self.match_score.player2.current_game.points] + 1
                        ]
                    )
                    if (
                            self.match_score.player2.current_game.points - self.match_score.player1.current_game.points
                    ) == 2:
                        self.match_score.player1.won_games += 1

    def __add_game(self, player_number: int):
        if player_number == 1:
            self.match_score.player1.won_games += 1
            if (
                    self.match_score.player1.won_games >= 4 and
                    ((self.match_score.player1.won_games - self.match_score.player2.won_games) >= 2)
            ):
                self.match_score.player1.won_games = 0
                self.__add_set(1)
        if player_number == 2:
            if (
                    self.match_score.player2.won_games >= 4 and
                    ((self.match_score.player2.won_games - self.match_score.player2.won_games) >= 2)
            ):
                self.match_score.player2.won_games = 0
                self.__add_set(2)

    def __add_set(self, player_number: int):
        if player_number == 1:
            self.match_score.player1.sets = self.match_score.player1.sets + 1
            if self.match_score.player1.sets == self.match_score.player2.sets:
                self.match_score.tie_break = True
            elif (self.match_score.player1.sets - self.match_score.player2.sets) == 2:
                self.match.winner = self.match.player1
        elif player_number == 2:
            self.match_score.player2.sets = self.match_score.player2.sets + 1
            if self.match_score.player1.sets == self.match_score.player2.sets:
                self.match_score.tie_break = True
            elif (self.match_score.player2.sets - self.match_score.player1.sets) == 2:
                self.match.winner = self.match.player2

    @staticmethod
    def __reset_game(player_game: GameDto) -> None:
        player_game.points = 0
        player_game.advantage = False


    def __add_tie_break_point(self, player_number: int):
        if player_number == 1:
            self.match_score.player1.current_game.points += 1
        elif player_number == 2:
            self.match_score.player1.current_game.points += 1

        if (
                self.match_score.player1.current_game.points >= 7 and
                ((self.match_score.player1.current_game.points - self.match_score.player2.current_game.points) >=2)
        ):
            self.match.winner = self.match.player1
        elif (
                self.match_score.player2.current_game.points >= 7 and
                ((self.match_score.player2.current_game.points - self.match_score.player1.current_game.points) >=2)
        ):
            self.match.winner = self.match.player2
