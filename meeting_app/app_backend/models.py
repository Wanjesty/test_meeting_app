from django.db import models

class User(models.Model):
    """Карточка пользователя"""
    image = models.ImageField("Фото", upload_to="avatars/")
    gender = models.CharField("Пол", max_length=10)
    name = models.CharField("Имя", max_length=100)
    surname = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Почта", max_length=255)
