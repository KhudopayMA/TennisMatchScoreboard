from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import redirect


class NewMatchPageView(View):
    def get(self, request, *args, **kwargs):
        t = render_to_string("tennis_match_scoreboard/new-match.html")
        return HttpResponse(t)

    def post(self, request, *args, **kwargs):
        t = render_to_string("tennis_match_scoreboard/new-match.html")
        return redirect("match_score", permanent=True)
