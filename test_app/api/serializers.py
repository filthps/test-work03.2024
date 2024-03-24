from rest_framework import serializers
from models import Text


class JSONSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)


class TextModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
