import re
from typing import Iterable, Optional, Union
from faker import Faker
from django.http import HttpRequest as DjangoRequest
from rest_framework.request import Request as DRFRequest
from .models import Text, Word


class Tools:
    request: Union[DjangoRequest, DRFRequest] = ...

    @property
    def is_ajax(self) -> bool:
        if not isinstance(self.request, (DjangoRequest, DRFRequest,)):
            raise TypeError
        if "X-Requested-With" in self.request.headers:
            if self.request.headers["X-Requested-With"] == "XMLHttpRequest":
                return True
        return False

    @staticmethod
    def generate_random_text() -> str:
        faker_ = Faker()
        random_text = faker_.text()
        return random_text


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
        def clean_words(words: list):
            reg = re.compile(r"\w+|[а-яА-Я]+", flags=re.S)
            while words:
                word: str = words.pop(0)
                if reg.match(word):
                    yield word.lower()
        words = re.split(r"\s", text, flags=re.MULTILINE)
        return [Word(text=text_instance, word=word) for word in clean_words(words)]

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
