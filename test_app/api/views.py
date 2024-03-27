import re
from faker import Faker
from typing import Iterable, Optional
from django.shortcuts import render, redirect
from django.db.transaction import atomic
from django.views.generic.base import TemplateView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from .models import Text, Word
from .serializers import JSONSerializer


class WordInstanceFactory:
    foreign_key_instance: Optional[Text] = None

    @classmethod
    def get_items(cls, data: dict):
        cls.__is_valid(data)
        if data["arr"]:
            return cls.__create_instances_best_case(cls.foreign_key_instance, data["arr"])
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
        if not any([data.get("arr", None), data.get("text", None)]):
            raise ValueError
        if data["arr"]:
            if not hasattr(data["arr"], "__iter__"):
                raise TypeError("Ожидалась итерируемая последовательность!")
            return
        if data["text"]:
            if type(data["text"]) is not str:
                raise TypeError


class FormPage(CreateAPIView, TemplateView):
    template_name = "form.html"
    http_method_names = ("get", "post",)
    renderer_classes = (HTMLFormRenderer, JSONRenderer,)
    serializer_class = JSONSerializer
    extra_context = {"form": JSONSerializer}

    def perform_create(self, serializer: JSONSerializer):
        with atomic():
            text_instance = Text.objects.create(add_by=self.request.user)
            WordInstanceFactory.foreign_key_instance = text_instance
            Word.objects.bulk_create(*WordInstanceFactory.get_items(serializer.data))


class Loader(ListAPIView):
    class Paginator(PageNumberPagination):
        page_size = 50
    pagination_class = Paginator
    serializer_class = JSONSerializer
    queryset = Word.objects.prefetch_related("text")


class GenerateTextView(APIView):  # ajax generate random text
    http_method_names = ("post",)

    def post(self, request):
        faker_ = Faker()
        random_text = faker_.text()
        if request.is_ajax:
            return Response(data=JSONSerializer(text=random_text), status=HTTP_200_OK)
        return Response(template_name="", status=HTTP_200_OK, data={"text": random_text})
