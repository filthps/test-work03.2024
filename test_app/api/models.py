import re
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


MAX_WORDS_COUNT = 200


def check_multi_words(s: str):
    words_count = len(re.match(r"\b^-", s).groups())
    if words_count > 1:
        raise ValidationError
    if words_count > MAX_WORDS_COUNT:
        raise ValidationError


class Text(models.Model):
    id = ...
    add_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}[{self.add_by.username}] {self.date.strftime('%Y-%m-%d %H:%M')}"


class Word(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True, max_length=30)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, blank=False, related_name="text_word")
    word = models.CharField(max_length=40, blank=False, validators=[check_multi_words])

    def __str__(self):
        return str(self.word)
