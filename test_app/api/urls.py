from django.urls import path
from .views import GenerateTextView, FormPage

urlpatterns = [
    path("", FormPage.as_view(), name="form"),
    path("get-text", GenerateTextView.as_view())  # ajax
]
