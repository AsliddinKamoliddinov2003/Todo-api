from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Todo, User



class TodoSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', "description", 'is_active']

        



class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fullname", "username", "password"]

    def is_valid(self, *args, **kwargs):
        valid = False
        if kwargs.get("username",None) and kwargs.get("password", None):
            return True
