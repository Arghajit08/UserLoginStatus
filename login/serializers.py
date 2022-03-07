from re import M
from django.db.models import fields
from rest_framework import serializers
from .models import MainUser

class UserSerializers(serializers.ModelSerializer):
    token=serializers.CharField(max_length=100,read_only=True)
    class Meta:
        model = MainUser
        fields = '__all__'