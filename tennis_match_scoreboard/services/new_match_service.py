from uuid import UUID
from typing import Optional

from tennis_match_scoreboard.models import Player, Match

class NewMatchService:
    """
    Service class for handling business logic related to NewMatchPageView view class.
    """

    @classmethod
    def create_match(cls, player1: Player, player2: Player) -> Optional[UUID]:
        player1 = Player.objects.get_or_create(name=player1)[0]
        player2 = Player.objects.get_or_create(name=player2)[0]
        match = Match.objects.create(player1=player1, player2=player2, score={})
        return match.uuid