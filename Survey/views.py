from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, View
from .models import Survey, Question, Answer, Response, Respondent
from users.models import CustomUser
from organization.models import OrgProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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


