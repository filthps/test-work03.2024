from django.urls import path
from .views import GenerateTextView, FormPage, StatisticPage

urlpatterns = [
    path("text-add/", FormPage.as_view(), name="form_page"),
    path("stats/total/", StatisticPage.as_view(), name="statistic"),
    path(r"stats/<int:textid>", StatisticPage.as_view(), name="statistic"),
    path(r"get-text/", GenerateTextView.as_view(), name="generate_text")  # ajax
]
