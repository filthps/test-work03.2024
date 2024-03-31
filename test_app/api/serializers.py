import re
from rest_framework import serializers
from .models import MAX_WORDS_COUNT


class JSONSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000, label="", required=False)
    arr = serializers.ListField(child=serializers.CharField(), min_length=1,
                                max_length=MAX_WORDS_COUNT, label="", required=False)

    def validate(self, data):
        print(self.initial_data)
        """ В зависимости от исправности функционала на стороне UI(фронт-енде),
        ожидается снять часть работы с бэк-енда, выполнив split строк на стороне UI.
        Таким образом: одно из полей сериализатора должно быть заполнено."""
        if "text" in self.initial_data and "arr" in self.initial_data:
            if not any([self.initial_data["text"], self.initial_data["arr"]]) or not all([self.initial_data["text"], self.initial_data["arr"]]):
                raise serializers.ValidationError("Пустая форма! Все поля пусты")
        if "text" not in self.initial_data and "arr" not in self.initial_data:
            raise serializers.ValidationError("Пустая форма. Полей нет")
        if self.initial_data["arr"]:
            re_ = re.compile(r"\b", flags=re.S)
            for word in self.initial_data["arr"]:
                if re_.match(word).groups():
                    raise serializers.ValidationError("С UI пришли недействительные данные!")
        return super().validate(self.initial_data)
