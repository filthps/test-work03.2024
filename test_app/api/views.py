import re
from typing import Iterable, Optional, Union
from faker import Faker
from django.shortcuts import render, redirect
from django.db.transaction import atomic
from django.db.models import Count, Value, F, Func, Subquery
from django.http import HttpRequest as DjangoRequest, HttpResponse
from django.views.generic.base import TemplateView
from rest_framework.request import Request as DRFRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from .models import Text, Word
from .serializers import AddTextSerializer, ViewWordSerializer


class Tools:
    @staticmethod
    def is_ajax(request: Union[DjangoRequest, DRFRequest]) -> Optional[bool]:
        if not isinstance(request, (DjangoRequest, DRFRequest,)):
            raise TypeError
        if "X-Requested-With" in request.headers:
            if request.headers["X-Requested-With"] == "XMLHttpRequest":
                return True


class WordInstanceFactory:
    foreign_key_instance: Optional[Text] = None

    @classmethod
    def get_items(cls, data: dict):
        cls.__is_valid(data)
        if data["words"]:
            return cls.__create_instances_best_case(cls.foreign_key_instance, data["words"])
        if data["text"]:
            return cls.__create_instances_emergency_case(cls.foreign_key_instance, data["text"])

    @staticmethod
    def __create_instances_best_case(text_instance: Text, data_arr: Iterable[str]) -> list[Word]:
        """ Текст разбит на слова на строне UI """
        return [Word(text=text_instance, word=word) for word in data_arr]

    @staticmethod
    def __create_instances_emergency_case(text_instance: Text, text: str) -> list[Word]:
        """ Запасной случай (на стороне UI не работает JavaScript) """
        items_arr = re.split(r"\b", text, flags=re.MULTILINE)
        return [Word(text=text_instance, word=word) for word in items_arr]

    @classmethod
    def __is_valid(cls, data: dict):
        if not isinstance(cls.foreign_key_instance, Text):
            raise TypeError
        if type(data) is not dict:
            raise TypeError
        if not any([data.get("words", None), data.get("text", None)]):
            raise ValueError
        if data["words"]:
            if not hasattr(data["words"], "__iter__"):
                raise TypeError("Ожидалась итерируемая последовательность!")
            return
        if data["text"]:
            if type(data["text"]) is not str:
                raise TypeError


class FormPage(CreateAPIView, TemplateView):
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
        qs.select_related("text").prefetch_related("text__add_by").values_list("word").annotate(  # values_list('word') - > GROUP BY word
            tf=Count(Value("word"), distinct=True) * "1." / Count(Value("word"), distinct=False)).values("word", "tf", "text_id", "text").annotate(
            user_id=F("text__add_by"), username=F("text__add_by__username"), idf=Func( function="LOG"))
        print(qs)
        return qs


class GenerateTextView(APIView, Tools):  # ajax generate random text
    http_method_names = ("post",)

    def post(self, request):
        faker_ = Faker()
        random_text = faker_.text()
        if self.is_ajax(request):
            return Response(data=AddTextSerializer(text=random_text), status=HTTP_200_OK)
        return Response(template_name="", status=HTTP_200_OK, data={"text": random_text})
