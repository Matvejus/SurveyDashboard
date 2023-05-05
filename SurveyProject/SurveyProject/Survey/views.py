from django.shortcuts import render
from .models import SurveyStatus
from .models import Survey
from .models import QuestionType
from .models import Question
from .models import QuestionOption
from .models import Respondent
from .models import Response
from .models import Answer 
from .models import AnswerOption

# Create your views here.

def index(request):
    survey_status = SurveyStatus.objects.all()
    context={'survey_status': survey_status} 
    return render(request, "index.html", context)

def index(request):
    surveys = Survey.objects.all()
    context={'surveys': surveys}
    return render(request, "index.html", context)

def index(request):
    question_type = QuestionType.objects.all()
    context={'question_type': question_type}
    return render(request, "index.html", context)

def index(request):
    questions = Question.objects.all()
    context={'questions': questions}
    return render(request, "index.html", context)

def index(request):
    question_option = QuestionOption.objects.all()
    context={'question_option': question_option}
    return render(request, "index.html", context)

def index(request):
    respondents = Respondent.objects.all()
    context={'respondents': respondents}
    return render(request, "index.html", context)

def index(request):
    responses = Response.objects.all()
    context={'responses': responses}
    return render(request, "index.html", context)

def index(request):
    answers = Answer.objects.all()
    context={'answers': answers}
    return render(request, "index.html", context)

def index(request):
    answer_option = AnswerOption.objects.all()
    context={'answer_option': answer_option}
    return render(request, "index.html", context)
