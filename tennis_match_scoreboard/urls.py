from django.urls import path

from .views import MainPageView, MatchesPageView, MatchScorePageView, NewMatchPageView

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("matches", MatchesPageView.as_view(), name="matches"),
    path("match-score", MatchScorePageView.as_view(), name="match_score"),
    path("new-match", NewMatchPageView.as_view(), name="new_match"),
]
