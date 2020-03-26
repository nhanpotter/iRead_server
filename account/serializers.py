from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

User = get_user_model()

class ActiveUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_active',)