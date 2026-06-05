import uuid

from django.db import models
from django.db.models import F, Q


class Players(models.Model):
    id = models.BigAutoField("ID", primary_key=True)
    name = models.CharField("Name", max_length=100)

    class Meta:
        db_table = "Players"


class Matches(models.Model):
    id = models.BigAutoField("ID", primary_key=True)
    uuid = models.UUIDField(
        "UUID",
        default=uuid.uuid4,
        editable=False
        )
    player1 = models.ForeignKey(Players, verbose_name="Player1", on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(Players, verbose_name="Player2", on_delete=models.CASCADE, related_name="player2")
    winner = models.ForeignKey(Players, verbose_name="Winner", on_delete=models.CASCADE)
    score = models.CharField("Score")

    class Meta:
        db_table = "Matches"
        constraints = [
            models.CheckConstraint(
                condition=~Q(player1=F("player2")),
                name="player1_not_player2"
            ),
            models.CheckConstraint(
                condition=Q(winner=F("player1")) | Q(winner=F("player2")),
                name="winner_must_be_player1_or_player2"
            ),
        ]
