from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('survey/<int:survey_id>/', views.survey_view, name='survey'), #change survey_id with survey to display
    # Add other URL patterns for the surveys app here
]
