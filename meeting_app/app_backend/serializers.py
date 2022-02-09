from django.db.models import fields
from rest_framework import serializers
from .models import Profile
from django_filters import rest_framework as filters
from math import sin, cos, radians, acos

class ProfileSerializer(serializers.ModelSerializer):
    
    distance = serializers.IntegerField()
    
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'name', 'surname', 'distance']


class SearchProfilesSerializer(serializers.ModelSerializer):
    
    #distance = serializers.IntegerField()
    
    
    class Meta:
        model = Profile
        fields = ['gender', 'name', 'surname']


class SearchProfilesFilter(filters.FilterSet):
    
    #distance = serializers.IntegerField()
    
    
    class Meta:
        model = Profile
        fields = ['gender', 'name', 'surname']