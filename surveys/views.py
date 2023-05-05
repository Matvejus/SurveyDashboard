from django.shortcuts import render
from .models import Survey, Question, Response

def survey_view(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    questions = Question.objects.filter(survey=survey)
    context = {
        'survey': survey,
        'questions': questions,
    }
    return render(request, 'surveys/survey.html', context)

def dashboard(request):
    surveys = Survey.objects.all()
    survey_responses = {}
    for survey in surveys:
        responses = Response.objects.filter(survey=survey)
        survey_responses[survey] = responses
    context = {
        'survey_responses': survey_responses,
    }
    return render(request, 'surveys/dashboard.html', context)