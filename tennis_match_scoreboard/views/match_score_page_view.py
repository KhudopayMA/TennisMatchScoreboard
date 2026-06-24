from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views import View

from tennis_match_scoreboard.dtos import MatchScoreDto
from tennis_match_scoreboard.models import Match
from tennis_match_scoreboard.services import ScoreService


class MatchScorePageView(View):
    def get(self, request: HttpRequest):
        match_uuid = request.COOKIES.get("match_uuid")
        if match_uuid is None:
            raise Http404("Match not found")
        match = Match.objects.get(uuid=match_uuid)
        match_score = MatchScoreDto(**match.score)
        return HttpResponse(
            render_to_string(
                "tennis_match_scoreboard/match-score.html",
                {
                    "player1": match.player1,
                    "player1_score": match_score.player1,
                    "player2": match.player2,
                    "player2_score": match_score.player2,
                },
            )
        )

    def post(self, request: HttpRequest):
        match_uuid = request.COOKIES.get("match_uuid")
        player_name = request.POST.get("player_name")
        if player_name is None:
            return HttpResponseBadRequest("player_name param not found in request.")
        score_service = ScoreService(match_uuid=match_uuid)
        if not score_service.match.winner:
            score_service.add_point(player_name=player_name)
        return HttpResponse(
            render_to_string(
                "tennis_match_scoreboard/match-score.html",
                {
                    "player1": score_service.match.player1,
                    "player1_score": score_service.match_score.player1,
                    "player2": score_service.match.player2,
                    "player2_score": score_service.match_score.player2,
                    "winner": score_service.match.winner,
                },
            )
        )
