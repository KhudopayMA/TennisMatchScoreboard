from django.urls import path

from .views import index, matches, match_score, new_match

urlpatterns = [
    path("", index, name="index"),
    path("matches", matches, name="matches"),
    path("match-score", match_score, name="match_score"),
    path("new-match", new_match, name="new_match"),
]