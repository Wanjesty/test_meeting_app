# Generated by Django 3.2.9 on 2021-12-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0005_auto_20211208_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female')], max_length=1, verbose_name='Пол'),
        ),
    ]
