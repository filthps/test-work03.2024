import re
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MAX_WORDS_COUNT, Text, Word


class AddTextSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000, label="", required=False, style={"base_template": "textarea.html", "rows": 5})
    words = serializers.ListField(child=serializers.CharField(), min_length=1,
                                  max_length=MAX_WORDS_COUNT, label="", required=False)

    def validate(self, data):

        """ В зависимости от исправности функционала на стороне UI(фронт-енде),
        ожидается снять часть работы с бэк-енда, выполнив split строк на стороне UI.
        Таким образом: одно из полей сериализатора должно быть заполнено."""
        if "text" in self.initial_data and "words" in self.initial_data:
            if not any([self.initial_data["text"], self.initial_data["words"]]) or not all([self.initial_data["text"], self.initial_data["words"]]):
                raise serializers.ValidationError("Пустая форма! Все поля пусты")
        if "text" not in self.initial_data and "words" not in self.initial_data:
            raise serializers.ValidationError("Пустая форма. Полей нет")
        if self.initial_data["words"]:
            re_ = re.compile(r"\b", flags=re.S)
            for word in self.initial_data["words"]:
                if re_.match(word).groups():
                    raise serializers.ValidationError("С UI пришли недействительные данные!")
        return super().validate(data)


class ViewWordSerializer(serializers.Serializer):
    text_id = serializers.ReadOnlyField()
    tf = serializers.ReadOnlyField()
    idf = serializers.ReadOnlyField()
    word = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
