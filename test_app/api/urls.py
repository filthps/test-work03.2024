from django.urls import path
from .views import GenerateTextView, FormPage

urlpatterns = [
    path("", FormPage.as_view(), name="form_page"),
    path("get-text", GenerateTextView.as_view(), name="generate_text")  # ajax
]
