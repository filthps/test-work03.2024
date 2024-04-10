import re
from rest_framework import serializers
from .tools import Tools
from .models import MAX_WORDS_COUNT


class Validation(serializers.Serializer):
    def validate(self, data):
        """ В зависимости от исправности функционала на стороне UI(фронт-енде),
        ожидается снять часть работы с бэк-енда, выполнив split строк на стороне UI.
        Таким образом: одно из полей сериализатора должно быть заполнено."""
        text = self.initial_data.get("text", None)
        words = self.initial_data.get("words", None)
        if not any([text, words]):
            raise serializers.ValidationError("Введите слова!")
        return super().validate(data)

    @staticmethod
    def validate_after_text_parse(status: bool):
        if not status:
            raise serializers.ValidationError("Из текста не удалось разобрать ни одного слова!")


class AddTextSerializer(Validation):
    text = serializers.CharField(label="", required=False, style={"base_template": "textarea.html", "rows": 5})
    words = serializers.ListField(child=serializers.CharField(), min_length=1,
                                  max_length=MAX_WORDS_COUNT, label="", required=False)


class AddTextSerializerNoAjax(AddTextSerializer):
    text = serializers.CharField(max_length=2000, label="", required=False, style={"base_template": "textarea.html", "rows": 5}, initial=Tools.generate_random_text)


class ViewWordSerializer(serializers.Serializer):
    text_id = serializers.ReadOnlyField()
    tf = serializers.ReadOnlyField()
    idf = serializers.ReadOnlyField()
    tf_idf = serializers.ReadOnlyField()
    word = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
