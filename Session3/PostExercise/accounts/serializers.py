from dataclasses import field
from rest_framework import serializers as sz
from .models import Major, Profile


class MajorSerializer(sz.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

class ProfileSerializer(sz.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
