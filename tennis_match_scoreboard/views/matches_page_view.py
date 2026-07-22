from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.views import View

from tennis_match_scoreboard.forms import MatchesFilterForm
from tennis_match_scoreboard.models import Match


class MatchesPageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        filter_form = MatchesFilterForm(request.GET)
        filter_form.is_valid()
        player_name = filter_form.cleaned_data["player_name"]
        if player_name:
            matches = Match.objects.filter(
                Q(player1__name=player_name) | Q(player2__name=player_name)
            ).select_related("player1", "player2").order_by("id")
        else:
            matches = Match.objects.all().select_related("player1", "player2").order_by("id")
        paginator = Paginator(matches, 5)
        request_page_number = request.GET.get("page")
        if request_page_number is None:
            page_number = 1
        else:
            page_number = int(request_page_number)
        page_matches = paginator.get_page(page_number)
        filter_form = MatchesFilterForm()
        t = render_to_string(
            "tennis_match_scoreboard/matches.html",
            {"matches": page_matches, "form": filter_form},
        )
        return HttpResponse(t)
