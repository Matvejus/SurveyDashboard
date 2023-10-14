from django.urls import path, include
from . import views
from .views import RegisterView



app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("", include("django.contrib.auth.urls")),
    path('edit_profile/<uuid:user_id>/', views.edit_profile, name='edit_profile'),
    path('redirectgroup/', views.redirectgroup, name='redirectgroup')
]

