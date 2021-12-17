import secrets
import string

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from .models import User,CodeType,Plan

# initializing size of string 
string_length = 7

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            contact=validated_data['contact']
        )
        # generating random strings 
        referralCode = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(string_length))
        user.referralCode=referralCode
        user.save()
        token = Token.objects.create(user=user)
        return user,token

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'contact',)


class CodeTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CodeType
        fields = ('id', 'codeType')


class PlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = ('id', 'plan_name', 'plan_code')
