from django.urls import path
from views import GenerateTextView, MainPage

urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("get-text", GenerateTextView.as_view())  # ajax
]
