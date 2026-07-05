from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from tennis_match_scoreboard.forms import NewMatchForm
from tennis_match_scoreboard.services import NewMatchService


@method_decorator(csrf_exempt, name='dispatch')
class NewMatchPageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = NewMatchForm()
        return HttpResponse(
            render_to_string(
                "tennis_match_scoreboard/new-match.html", {"form": form}
            )
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = NewMatchForm(request.POST)
        if form.is_valid() and not form.errors:
                match_uuid = NewMatchService.create_match(
                    player1=form.cleaned_data["player1"],
                    player2=form.cleaned_data["player2"],
                )
                url = (
                    reverse("match_score")
                    + "?"
                    + urlencode({"uuid": match_uuid})
                )
                response = redirect(url, uuid=match_uuid, permanent=True)
                response.set_cookie("match_uuid", str(match_uuid))
                return response

        return HttpResponse(
            render_to_string(
                "tennis_match_scoreboard/new-match.html", {"form": form}
            )
        )
