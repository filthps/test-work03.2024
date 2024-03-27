import re
from rest_framework import serializers
from .models import MAX_WORDS_COUNT


class JSONSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000, label="")
    arr = serializers.ListField(child=serializers.CharField(), allow_empty=False, min_length=1,
                                max_length=MAX_WORDS_COUNT, label="")

    def validate(self, attrs):
        """ В зависимости от исправности функционала на стороне UI(фронт-енде),
        ожидается снять часть работы с бэк-енда, выполнив split строк на стороне UI.
        Таким образом: одно из полей сериализатора должно быть заполнено."""
        if not any([attrs["text"], attrs["arr"]]) or all([attrs["text"], attrs["arr"]]):
            raise serializers.ValidationError
        if attrs["arr"]:
            re_ = re.compile(r"\b", flags=re.S)
            for word in attrs["arr"]:
                if re_.match(word).groups():
                    raise serializers.ValidationError("С UI пришли недействительные данные!")
