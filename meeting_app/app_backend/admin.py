from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Карточка пользователя"""
    
    fields = ['user', 'image', 'gender', 'name', 'surname', 'email']
    list_display = ['user', 'image', 'gender', 'name', 'surname', 'email']