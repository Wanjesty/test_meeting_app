from django.contrib import admin
from .models import Profile, Profile_evaluations

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Карточка пользователя"""
    
    fields = ['user', 'image', 'gender', 'name', 'surname', 'email'] #Поля для ввода данных
    list_display = ['pk', 'user', 'image', 'gender', 'name', 'surname', 'email'] #Поля для просмотра данных

@admin.register(Profile_evaluations)
class Profile_evaluationsAdmin(admin.ModelAdmin):
    """Лайки и дазлайки пользователя"""
    list_display = ['pk', 'user', 'liked_profiles', 'disliked_profiles']