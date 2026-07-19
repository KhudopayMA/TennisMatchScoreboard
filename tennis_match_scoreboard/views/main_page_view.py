from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "tennis_match_scoreboard/index.html"
