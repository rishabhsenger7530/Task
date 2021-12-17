from django.shortcuts import render
from rest_framework import viewsets
from .models import TelecomApi
from .serializers import TelecomApiSerializers



#views start
class CreateTelecomeView(viewsets.ModelViewSet):
    queryset = TelecomApi.objects.all()
    serializer_class = TelecomApiSerializers
