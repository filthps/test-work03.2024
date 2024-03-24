from faker import Faker
from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from .models import Text
from .serializers import JSONSerializer, TextModelSerializer


class MainPage(APIView):
    http_method_names = ("get", "post",)

    def get(self, request):
        if request.is_ajax:
        return Response(status=HTTP_200_OK, template_name="")

    def post(self, request):
        form_data = request.POST.get("text")
        serializer = TextModelSerializer(data={"text": form_data})
        if not serializer.is_valid():
            serializer.create(serializer.data)
            return Response(status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return Response(template_name="templates/stat.html", status=HTTP_201_CREATED, data=serializer.data)



class Loader(ListAPIView):
    class Paginator(PageNumberPagination):
        page_size = 50
    pagination_class = Paginator
    serializer_class = JSONSerializer
    queryset = Text.objects.all()

    def get_queryset(self):
        pass

    def get(self, request):
        pass

class GenerateTextView(APIView):  # ajax generate random text
    http_method_names = ("post",)

    def post(self, request):
        faker_ = Faker()
        random_text = faker_.text()
        if request.is_ajax:
            return Response(data=JSONSerializer(text=random_text), status=HTTP_200_OK)
        return Response(template_name="", status=HTTP_200_OK, data={"text": random_text})
