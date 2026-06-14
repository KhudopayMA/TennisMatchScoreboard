from urllib.parse import urlencode

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect

from tennis_match_scoreboard.forms import NewMatchForm
from tennis_match_scoreboard.services import NewMatchService


class NewMatchPageView(View):
    def get(self, request, *args, **kwargs):
        form = NewMatchForm()
        return HttpResponse(
            render_to_string("tennis_match_scoreboard/new-match.html", {"form": form})
        )

    def post(self, request, *args, **kwargs):
        form = NewMatchForm(request.POST)
        if form.is_valid():
            if not form.errors:
                match_uuid = NewMatchService.create_match(
                    player1=form.cleaned_data["player1"],
                    player2=form.cleaned_data["player2"]
                )
                url = reverse("match_score") + "?" + urlencode({"uuid": match_uuid})
                return redirect(url, uuid=match_uuid, permanent=True)

        return HttpResponse(
            render_to_string("tennis_match_scoreboard/new-match.html", {"form": form})
        )
