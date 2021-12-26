from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image


"""def get_upload_file(instance, filename): #Собирает путь для хранения image пользователей   
    return os.path.join("app_backend/user_avatars/", f"{instance.user}/", filename)"""


class Profile(models.Model):
    """Карточка пользователя"""
    CHOICES = (
        ("m", "male"),
        ("f", "female")
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    image = models.ImageField("Фото", upload_to="app_backend/user_avatars/", blank=True)
    gender = models.CharField("Пол", max_length=1,choices=CHOICES, blank=True)
    name = models.CharField("Имя", max_length=100, blank=True)
    surname = models.CharField("Фамилия", max_length=100, blank=True)
    email = models.EmailField("Почта", max_length=255, blank=True)