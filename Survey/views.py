from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View
from .models import (Survey, Question, QuestionOption, Answer, Response, Respondent)
from .forms import AnswerForm
from users.models import CustomUser
from organization.models import OrgProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic.edit import CreateView




# add views here

class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'survey_list.html'  # Assuming you have this template
    context_object_name = 'surveys'  # This is the name of the list in the template

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Get the surveys related to the user's organization
        return Survey.objects.filter(org_profiles__in=[user.organization])

@method_decorator(login_required, name='dispatch')
class SurveyDetailView(View):
    template_name = 'survey/survey_detail.html'

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=kwargs.get('pk'), survey_name_slug=kwargs.get('survey_name'))
        questions = survey.question_set.all()
        context = {
            'survey': survey,
            'questions': questions,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class SurveySubmitView(View):
    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, pk=kwargs.get('pk'), survey_name_slug=kwargs.get('survey_name'))
        questions = survey.question_set.all()

        # Get the OrgProfile object for the currently logged in user
        organization = request.user.organization

        # Create a new Respondent object
        respondent = Respondent(user=request.user, organization=organization)
        respondent.save()

        # Create a new Response object
        response = Response(respondent=respondent, survey=survey)
        response.save()

        # Create Answer objects for each question
        for question in questions:
            answer_text = request.POST.get(f'answer-{question.pk}')
            if answer_text:
                answer = Answer(
                    response=response,
                    question=question,
                    answer=answer_text,
                    user=request.user,
                    organization=organization,
                    survey=survey,
                )
                answer.save()

        messages.success(request, "Your answers have been submitted!")
        return redirect('/survey_detail')


""" #Haley's view for taking a survey:
def show_survey(request, id=None):
    survey = get_object_or_404(Survey, pk=id)
    post_data = request.POST if request.method == "POST" else None
    form = SurveyForm(survey)

    url = reverse("show_survey", args=(id,))
    if form.is_bound and form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, "Submissions saved.")
        return redirect(url)

    context = {
        "survey": survey,
        "form": form,
    }
    return render(request, "Survey/survey.html", context) """



class SurveyView(CreateView):    

    def get(self, request, *args, **kwargs):
        survey = Survey.objects.get(pk=1)
        questions = survey.question_set.all().values()
        #to load all question options of particular survey 
        #need to add foreign key in questionoption modled to connect to survey
        questionoptions = QuestionOption.objects.all().values()
        #to get set of of options for particular question:
        q_full = []
        for q in questions.values():
            q['options'] = questionoptions.filter(question_id = q['id']).values_list('option_text', flat = True)
            q_full.append(q)

        context = {
            "survey": survey,
            "questions": q_full,
        }
        return render(request, "survey/take-survey.html", context)

        
    def post(self, request, *args, **kwargs):
        form = AnswerForm()
        if form.is_valid():
            if form.is_valid():
                new_survey = form.save(commit = False)
                new_survey.organization = request.user.organization  
                new_survey.save()
                return redirect('organization:profile')

        return render(request, "survey/take-survey.html", {"form": form} )

    

    #def save: on click save answers and attach saved answers/users/org/time to response model

    

    