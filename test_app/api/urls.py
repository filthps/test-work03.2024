from django.urls import path
from django.views.generic.base import RedirectView
from .views import GenerateTextView, FormPage, StatisticPage

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="form_page", permanent=True), name="main"),
    path("text-add/", FormPage.as_view(), name="form_page"),
    path("stats/", RedirectView.as_view(pattern_name="statistic"), name="statistic"),
    path("stats/total/", StatisticPage.as_view(), name="statistic"),
    path(r"stats/<int:textid>", StatisticPage.as_view(), name="statistic"),
    path(r"get-text/", GenerateTextView.as_view(), name="generate_text")  # ajax
]
