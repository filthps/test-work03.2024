from django.db.transaction import atomic
from django.db.models import Count, Value, F, Func, FloatField
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Text, Word
from .serializers import AddTextSerializer, AddTextSerializerNoAjax, ViewWordSerializer
from .tools import Tools, WordInstanceFactory


class FormPage(LoginRequiredMixin, CreateAPIView, TemplateView, Tools):
    login_url = "/admin/"
    template_name = "form.html"
    http_method_names = ("get", "post",)
    serializer_class = AddTextSerializer
    extra_context = {"form": AddTextSerializer}
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer: AddTextSerializer) -> int:
        with atomic():
            text_instance = Text.objects.create(add_by=self.request.user)
            WordInstanceFactory.foreign_key_instance = text_instance
            word_model_instance_collection = WordInstanceFactory.get_items(dict(serializer.data))
            Word.objects.bulk_create(word_model_instance_collection)
        return text_instance.id

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text_pk = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return HttpResponse("statistic", text_pk, status=HTTP_201_CREATED, headers=headers)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if "gentext" in self.request.query_params:
            kwargs.update({"form": AddTextSerializerNoAjax})
        return kwargs


class StatisticPage(ListAPIView, TemplateView):
    class Paginator(PageNumberPagination):
        page_size = 50
    http_method_names = ("get",)
    pagination_class = Paginator
    template_name = "stat.html"
    serializer_class = ViewWordSerializer

    def list(self, *args, **kwargs):
        self.request.text_id = kwargs.get("textid", None)
        response_instance: Response = super().list(*args, **kwargs)
        return Response(status=HTTP_200_OK, data={"data": response_instance.data})

    def get_queryset(self):
        total_text_count = Text.objects.count()
        qs = Word.objects.all()
        if self.request.text_id is not None:
            qs = Word.objects.filter(text_id=self.request.text_id)
        qs = qs.select_related("text").prefetch_related("text__add_by").values("word").annotate(  # values('word') - > GROUP BY word
            tf=(Count(Value("word"), distinct=False) / Count(Value("word"), distinct=True)) * .1).values("word", "tf", "text_id", "text").annotate(
            user_id=F("text__add_by"), username=F("text__add_by__username"),
            idf=Func(Value(total_text_count), Count("word", distinct=False),
                     function="LOG", output_field=FloatField()), tf_idf=F("tf") * F("idf")).order_by("-idf")
        return qs


class GenerateTextView(APIView, TemplateView, Tools):  # ajax generate random text
    http_method_names = ("post",)

    def post(self, *args):
        if self.is_ajax:
            return Response({"text": self.generate_random_text()}, status=HTTP_200_OK, content_type="application/json")
        return redirect(reverse("form_page") + "?gentext")  # todo: fixit в броузере не меняется текущий URL
