from pyexpat import model
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from app_backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/clients/", include("app_backend.urls")),
    path("api/list/<int:user_id>/", views.ProfilesListView.as_view()),
    #path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)