from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Карточка пользователя"""
    
    fields = ['user', 'image', 'gender', 'name', 'surname', 'email'] #Поля для ввода данных
    list_display = ['pk', 'user', 'image', 'gender', 'name', 'surname', 'email'] #Поля для просмотра данных