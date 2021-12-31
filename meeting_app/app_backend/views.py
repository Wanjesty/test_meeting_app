from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
import os, shutil
from PIL import Image


from .serializers import ProfileSerializers
from .models import Profile, Profile_evaluations

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
            profile.image = add_watermark(request)
        profile.save()
        return HttpResponse("User created", status=status.HTTP_201_CREATED)


class DeleteUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        users = User.objects.filter(username=username)
        if users:
            user = users[0]
            if user.check_password(password):
                user.delete()
                path = os.path.join("app_backend/user_avatars/", f'{username}')
                shutil.rmtree(path)
                return HttpResponse("User deleted", status=status.HTTP_200_OK)
            else:
                return HttpResponse("Invalid password", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Invalid username", status=status.HTTP_200_OK)


class ChangeUserProfileView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        users = User.objects.filter(username=username)
        if users:
            user = users[0]
            if user.check_password(password):
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
                    profile.image = add_watermark(request)
                profile.save()
                return HttpResponse("User profile changed", status=status.HTTP_200_OK)
            else:
                return HttpResponse("Invalid password", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Invalid username", status=status.HTTP_200_OK)


class ProfileAssessmentView(APIView): #Оценка пользователя другим пользователем
    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializers(profile)
        return Response(serializer.data)
    def post(self, request, pk):
        username = request.data.get("username") #Ввод в переменные данных оценивающего пользователя
        password = request.data.get("password")
        users = User.objects.filter(username=username)
        if users: # Проверка на существование оценивающего пользователя
            user = users[0]
            if user.check_password(password): # Проверка пароля
                profile_for_assessment = Profile_evaluations.objects.filter(pk=pk) # Поиск профиля для оценки в БД
                if profile_for_assessment:
                    if request.data.get("assessment") == "like":
                        user_evalutions = Profile_evaluations.objects.get(user=user)
                        likes = user_evalutions.liked_profiles
                        likes.append(pk)
                        user_evalutions.liked_profiles = likes
                        user_evalutions.save()
                        if user_evalutions.pk in profile_for_assessment[0].liked_profiles:
                            liked_profile = Profile.objects.get(pk=pk)
                            profile = Profile.objects.get(user=user)
                            liked_profile.mutual_sympathy.add(profile)
                            liked_profile.save()
                            profile.mutual_sympathy.add(liked_profile)
                            profile.save()
                            return HttpResponse(f"Mutual sympathy, email: {liked_profile.email}", status=status.HTTP_200_OK)
                        return HttpResponse("Profile liked", status=status.HTTP_200_OK)
                    elif request.data.get("assessment") == "dislike":
                        user_evalutions = Profile_evaluations.objects.get(user=user)
                        dislikes = user_evalutions.disliked_profiles
                        dislikes.append(pk)
                        user_evalutions.disliked_profiles = dislikes
                        user_evalutions.save()
                        return HttpResponse("Profile dislaked", status=status.HTTP_200_OK)
                else:
                    return HttpResponse("No such profile", status=status.HTTP_200_OK)



def add_watermark(request): #Добавление ватермарки на картинку
    base_image = Image.open(request.data.get('image')).convert("RGBA")
    watermark = Image.open((os.path.abspath("app_backend/user_avatars/watermark.png"))).convert("RGBA")
    save_path = os.path.join("app_backend/user_avatars/", f"{request.data.get('username')}/", f"{request.data.get('image')}")
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    transparent.paste(watermark, (0, 0), mask=watermark)
    try:
        transparent.save(save_path)
    except FileNotFoundError:
        os.mkdir("app_backend/user_avatars/" + f"{request.data.get('username')}/")
        transparent.save(save_path)
    return save_path