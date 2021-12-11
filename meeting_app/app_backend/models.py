from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Карточка пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    image = models.ImageField("Фото", upload_to="avatars/", blank=True)
    gender = models.CharField("Пол", max_length=10, blank=True)
    name = models.CharField("Имя", max_length=100, blank=True)
    surname = models.CharField("Фамилия", max_length=100, blank=True)
    email = models.EmailField("Почта", max_length=255, blank=True)
