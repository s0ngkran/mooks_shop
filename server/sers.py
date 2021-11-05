from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class TokenSer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class PromotionOnGroupSer(serializers.ModelSerializer):
    class Meta:
        model = PromotionOnGroup
        fields = '__all__'