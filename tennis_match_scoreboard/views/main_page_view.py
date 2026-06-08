from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        t = render_to_string("tennis_match_scoreboard/index.html")
        return HttpResponse(t)
