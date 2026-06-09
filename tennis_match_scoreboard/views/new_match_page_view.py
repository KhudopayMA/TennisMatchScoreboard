from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import redirect

from tennis_match_scoreboard.forms import NewMatchForm
from tennis_match_scoreboard.services import NewMatchService


class NewMatchPageView(View):
    def get(self, request, *args, **kwargs):
        form = NewMatchForm()
        t = render_to_string("tennis_match_scoreboard/new-match.html", {"form": form})
        return HttpResponse(t)

    def post(self, request, *args, **kwargs):
        form = NewMatchForm(request.POST)
        if form.is_valid():
            NewMatchService
            t = render_to_string("tennis_match_scoreboard/new-match.html")
            return redirect("match_score", permanent=True)

        return HttpResponse(
            render_to_string("tennis_match_scoreboard/new-match.html", {"form": form})
        )
