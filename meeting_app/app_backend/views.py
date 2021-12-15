from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse

from .models import Profile

class RegisterUserView(APIView):
    def post(self, request):
        user = User.objects.create(
            username=request.data.get('username')
        )
        user.set_password(str(request.data.get('password')))
        user.save()
        user_profile = User.objects.get(username = request.data.get('username'))
        profile = Profile.objects.get(user = user_profile)
        if 'gender' in request.data:
            profile.gender = request.data.get('gender')
        if 'name' in request.data:
            profile.name = request.data.get('name')
        if 'surname' in request.data:
            profile.surname = request.data.get('surname')
        if 'email' in request.data:
            profile.email = request.data.get('email')
        if 'image' in request.data:
            profile.image = request.data.get('image')
        profile.save()
        return HttpResponse("User created", status=status.HTTP_201_CREATED)