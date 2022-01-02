"""from .models import Profile, Profile_evaluations
from django.contrib.auth.models import User


class DataUser:
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
        self.save_model_Profile_evaluations.liked_profiles = self.liked_profiles
        self.save_model_Profile_evaluations.disliked_profiles = self.disliked_profiles
        self.save_model_User.save()
        self.save_model_Profile.save()
        self.save_model_Profile_evaluations.save() """ 