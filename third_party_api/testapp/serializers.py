from rest_framework import serializers
from .models import TelecomApi

class TelecomApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = TelecomApi
        fields = ("id", "code","price",)
