from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.core.paginator import Paginator

from tennis_match_scoreboard.models import Match


class MatchesPageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        filter_by_player_name = request.GET.get("filter_by_player_name")
        if filter_by_player_name:
            matches = Match.objects.filter(Match.player1.name == filter_by_player_name) | Match.objects.filter(Match.player2.name == filter_by_player_name)
        else:
            matches = Match.objects.all()
        paginator = Paginator(matches, 5)
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 1
        page_matches = paginator.get_page(page_number)
        t = render_to_string("tennis_match_scoreboard/matches.html", {"matches": page_matches})
        return HttpResponse(t)
