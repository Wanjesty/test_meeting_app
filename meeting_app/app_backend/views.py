from email import charset
from operator import index
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status, generics, filters
from rest_framework.response import Response
from django.http import HttpResponse
import os, shutil
from PIL import Image
import smtplib
from math import sin, cos, radians, acos, sqrt
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, ExpressionWrapper, FloatField, Func

from .serializers import ProfileSerializer, SearchProfilesSerializer
from .models import Profile, Profile_evaluations


class DataUser: #Класс для хранения данных об учатнике
    def __init__(self, pk):
        self.pk = pk
        self.model_User = User.objects.get(pk=pk)
        self.model_Profile = Profile.objects.get(pk=pk)
        self.model_Profile_evaluations = Profile_evaluations.objects.get(pk=pk)
        self.username = self.model_User.username
        self.image = self.model_Profile.image
        self.gender = self.model_Profile.gender
        self.name = self.model_Profile.name
        self.surname = self.model_Profile.surname
        self.email = self.model_Profile.email
        self.longitude = self.model_Profile.longitude
        self.latitude = self.model_Profile.latitude
        self.mutual_sympathy = self.model_Profile.mutual_sympathy.all()
        self.liked_profiles = self.model_Profile_evaluations.liked_profiles
        self.disliked_profiles = self.model_Profile_evaluations.disliked_profiles
    
    
    def add_mutual_sympathy(self, profile):
        self.save_model_Profile = Profile.objects.get(pk=self.pk)
        self.save_model_Profile.mutual_sympathy.add(profile)
        self.save_model_Profile.save()

    def save(self):
        self.save_model_User = User.objects.get(pk=self.pk)
        self.save_model_Profile = Profile.objects.get(pk=self.pk)
        self.save_model_Profile_evaluations = Profile_evaluations.objects.get(pk=self.pk)
        self.save_model_Profile.image = self.image
        self.save_model_Profile.gender = self.gender
        self.save_model_Profile.name = self.name
        self.save_model_Profile.surname = self.surname
        self.save_model_Profile.email = self.email
        self.save_model_Profile.longitude = self.longitude
        self.save_model_Profile.latitude = self.latitude
        self.save_model_Profile_evaluations.liked_profiles = self.liked_profiles
        self.save_model_Profile_evaluations.disliked_profiles = self.disliked_profiles
        self.save_model_User.save()
        self.save_model_Profile.save()
        self.save_model_Profile_evaluations.save()


class RegisterUserView(APIView): #Регистрация участника
    def post(self, request):
        user = User.objects.create(
            username=request.data.get('username')
        )
        user.set_password(str(request.data.get('password')))
        user.save()
        user_profile = User.objects.get(username = request.data.get('username'))
        created_user = DataUser(user_profile.pk)
        if 'gender' in request.data:
            created_user.gender = request.data.get('gender')
        if 'name' in request.data:
            created_user.name = request.data.get('name')
        if 'surname' in request.data:
            created_user.surname = request.data.get('surname')
        if 'email' in request.data:
            created_user.email = request.data.get('email')
        if 'image' in request.data:
            created_user.image = add_watermark(request)
        if 'longitude' in request.data:
            created_user.longitude = float(request.data.get('longitude'))
        if 'latitude' in request.data:
            created_user.latitude = float(request.data.get('latitude'))
        created_user.save()
        return HttpResponse("User created", status=status.HTTP_201_CREATED)


class DeleteUserView(APIView): #Удаление участника
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


class ChangeUserProfileView(APIView): #Изменение данных об учатнике
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        users = User.objects.filter(username=username)
        if users:
            user = users[0]
            if user.check_password(password):
                modifiable_user = DataUser(user.pk)
                if 'gender' in request.data:
                    modifiable_user.gender = request.data.get('gender')
                if 'name' in request.data:
                    modifiable_user.name = request.data.get('name')
                if 'surname' in request.data:
                    modifiable_user.surname = request.data.get('surname')
                if 'email' in request.data:
                    modifiable_user.email = request.data.get('email')
                if 'image' in request.data:
                    modifiable_user.image = add_watermark(request)
                if 'longitude' in request.data:
                    modifiable_user.longitude = float(request.data.get('longitude'))
                if 'latitude' in request.data:
                    modifiable_user.latitude = float(request.data.get('latitude'))
                modifiable_user.save()
                return HttpResponse("User profile changed", status=status.HTTP_200_OK)
            else:
                return HttpResponse("Invalid password", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Invalid username", status=status.HTTP_200_OK)


class ProfileAssessmentView(APIView): #Оценка пользователя другим пользователем
    
    def post(self, request, pk):
        username = request.data.get("username") #Ввод в переменные данных оценивающего пользователя
        password = request.data.get("password")
        users = User.objects.filter(username=username)
        if users: # Проверка на существование оценивающего пользователя
            user = users[0]
            if user.check_password(password): # Проверка пароля
                profile_for_assessment = Profile_evaluations.objects.filter(pk=pk) # Поиск профиля для оценки в БД
                if profile_for_assessment:
                    rating_user = DataUser(user.pk)
                    user_to_rate = DataUser(pk)
                    if "assessment" in request.data:
                        if request.data.get("assessment") == "like":
                            rating_user.liked_profiles.append(user_to_rate.pk)
                            rating_user.save()
                            if rating_user.pk in user_to_rate.liked_profiles:
                                rating_user.add_mutual_sympathy(user_to_rate.model_Profile)
                                user_to_rate.add_mutual_sympathy(rating_user.model_Profile)
                                send_emails(rating_user, user_to_rate)
                                return HttpResponse(f"Mutual sympathy, email: {user_to_rate.email}", status=status.HTTP_200_OK)
                            return HttpResponse("Profile liked", status=status.HTTP_200_OK)
                        elif request.data.get("assessment") == "dislike":
                            rating_user.disliked_profiles.append(user_to_rate.pk)
                            rating_user.save()
                            return HttpResponse("Profile dislaked", status=status.HTTP_200_OK)
                    else:
                        range_between_users = calc_dist(rating_user.latitude, rating_user.longitude, user_to_rate.latitude, user_to_rate.longitude)
                        profile = Profile.objects.values().get(pk=pk)
                        profile['distance'] = int(range_between_users)
                        serializer = ProfileSerializer(data=profile)
                        if serializer.is_valid():
                            return Response(serializer.data)
                else:
                    return HttpResponse("No such profile", status=status.HTTP_200_OK)


class ProfilesListView(generics.ListAPIView): #Сортировка участников по параметрам в search_fields
    def get_queryset(self):
        user_id = ''
        for char in self.request.path_info[10:]:
            if char != '/':
                user_id += char
            else:
                break
        user_id = int(user_id)
        try:
            distance = int(self.request.GET.get('distance'))
            current_user = DataUser(user_id)
            lon1 = current_user.longitude - distance / abs(cos(radians(current_user.latitude)) * 111.0)
            lon2 = current_user.longitude + distance / abs(cos(radians(current_user.latitude)) * 111.0)
            lat1 = current_user.latitude - (distance / 111.0)
            lat2 = current_user.latitude + (distance / 111.0)
            queryset = Profile.objects.filter(latitude__range=(lat1, lat2)).filter(longitude__range=(lon1, lon2))
            return queryset
        except TypeError:
            queryset = Profile.objects.all()
            return queryset
    
    serializer_class = SearchProfilesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender', 'name', 'surname']

        

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


def send_emails(first_user, second_user): #Отправка сообщений пользователям со взаимной симпатией
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('denisburkovfortest@gmail.com','Denisfortest2022')
    msg1 = f"Mutual sympathy with {second_user.name}, email: {second_user.email}"
    msg2 = f"Mutual sympathy with {first_user.name}, email: {first_user.email}"
    smtpObj.sendmail("denisburkovfortest@gmail.com", first_user.email, msg1)
    smtpObj.sendmail("denisburkovfortest@gmail.com", second_user.email, msg2)
    smtpObj.quit()


def calc_dist(lat_a, long_a, lat_b, long_b):
    earth_radius_in_km = 6371
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
        )
    return acos(cos_x) * earth_radius_in_km
