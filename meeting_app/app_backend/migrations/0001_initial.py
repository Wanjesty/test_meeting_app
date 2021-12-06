# Generated by Django 3.2.9 on 2021-12-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatars/', verbose_name='Фото')),
                ('gender', models.CharField(max_length=10, verbose_name='Пол')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=255, verbose_name='Почта')),
            ],
        ),
    ]