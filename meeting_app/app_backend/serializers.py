from django.db.models import fields
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'name', 'surname']


class SearchFilterProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'name', 'surname']
