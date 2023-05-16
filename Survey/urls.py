from django.urls import path
from .views import SurveyListView, SurveyDetailView, SurveySubmitView

app_name = 'survey'
urlpatterns = [
    path('survey/', SurveyListView.as_view(), name='survey_list'),
    path('<slug:survey_name>/<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('<slug:survey_name>/<int:pk>/submit/', SurveySubmitView.as_view(), name='survey_submit'),
]