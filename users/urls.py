from django.urls import path, include
from . import views
from .views import RegisterView, update_user_profile



app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("", include("django.contrib.auth.urls")),
    path('edit_profile/', update_user_profile.as_view(), name='edit_profile'),
    path('redirectgroup/', views.redirectgroup, name='redirectgroup')
]

