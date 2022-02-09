from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.RegisterUserView.as_view()),
    path("<int:pk>/match/", views.ProfileAssessmentView.as_view()),
    path("delete/", views.DeleteUserView.as_view()),
    path("change/", views.ChangeUserProfileView.as_view()),  
]