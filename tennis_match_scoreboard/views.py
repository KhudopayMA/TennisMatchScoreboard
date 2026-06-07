from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    t = render_to_string("tennis_match_scoreboard/index.html")
    return HttpResponse(t)

def new_match(request):
    t = render_to_string("tennis_match_scoreboard/new-match.html")
    return HttpResponse(t)

def match_score(request):
    t = render_to_string("tennis_match_scoreboard/match-score.html")
    return HttpResponse(t)

def matches(request):
    t = render_to_string("tennis_match_scoreboard/matches.html")
    return HttpResponse(t)
