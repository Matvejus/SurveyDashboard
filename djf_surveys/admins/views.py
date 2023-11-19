import csv
from io import StringIO

from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.template.loader import render_to_string

from djf_surveys.app_settings import SURVEYS_ADMIN_BASE_PATH
from djf_surveys.models import Survey, Question, UserAnswer, TYPE_FIELD, Dimension, SubDimension
from djf_surveys.mixin import ContextTitleMixin
from djf_surveys.views import SurveyListView
from djf_surveys.forms import BaseSurveyForm, SurveyForm, QuestionForm, QuestionWithChoicesForm
from djf_surveys.summary import SummaryResponse



def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminCreateSurveyView(ContextTitleMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'djf_surveys/admins/form.html'
    title_page = _("Add New Survey")

    def get_success_url(self):
        return reverse_lazy("djf_surveys:admin_forms_survey", args=[self.object.slug])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext("%(page_action_name)s succeeded.") % {'page_action_name': capfirst(self.title_page.lower())})
        return response

    def form_invalid(self, form):
        messages.error(self.request, _("There were some errors in your form. Please correct them."))
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = self.title_page
        return context


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminEditSurveyView(ContextTitleMixin, UpdateView):
    model = Survey
    template_name = 'djf_surveys/admins/form.html'
    fields = [
        'name', 'description', 'editable', 'deletable', 
        'duplicate_entry', 'private_response', 'can_anonymous_user'
    ]
    title_page = _("Edit Survey")

    def get_success_url(self):
        survey = self.get_object()
        return reverse("djf_surveys:admin_forms_survey", args=[survey.slug])


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminSurveyListView(SurveyListView):
    template_name = 'djf_surveys/admins/survey_list.html'


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminSurveyFormView(ContextTitleMixin, FormMixin, DetailView):
    model = Survey
    template_name = 'djf_surveys/admins/form_preview.html'
    form_class = BaseSurveyForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.object, user=self.request.user, **self.get_form_kwargs())

    def get_title_page(self):
        return self.object.name

    def get_sub_title_page(self):
        return self.object.description


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminDeleteSurveyView(DetailView):
    model = Survey

    def get(self, request, *args, **kwargs):
        survey = self.get_object()
        survey.delete()
        messages.success(request, gettext("Survey %ss succesfully deleted.") % survey.name)
        return redirect("djf_surveys:admin_survey")

    
def load_dimensions(request):
    level_id = request.GET.get('level')
    dimensions = Dimension.objects.filter(level__id=level_id).order_by('id')
    return render(request, 'admins/dimension_dropdown_list_options.html', {'dimensions': dimensions})

def load_subdimensions(request):
    dimension_id = request.GET.get('dimension')
    dimension = Dimension.objects.get(id=dimension_id)
    subdimensions = dimension.sub_dimensions.all().order_by('id')
    return render(request, 'admins/sub_dimension_dropdown_list_options.html', {'subdimensions': subdimensions})


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator', 'Supervisor'])], name='dispatch')
class AdminCreateQuestionView(ContextTitleMixin, CreateView):
    template_name = 'djf_surveys/admins/question_form.html'
    success_url = reverse_lazy("djf_surveys:")
    title_page = _("Add Question")
    survey = None
    type_field_id = None

    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, id=kwargs['pk'])
        self.type_field_id = kwargs['type_field']
        self.object = None
        if self.type_field_id not in TYPE_FIELD:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        choices = [TYPE_FIELD.multi_select, TYPE_FIELD.select, TYPE_FIELD.radio]
        if self.type_field_id in choices:
            return QuestionWithChoicesForm
        else:
            return QuestionForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if 'dimension' in request.POST:
            dimension_id = request.POST.get('dimension')
            form.fields['subdimension'].queryset = SubDimension.objects.filter(dimension__id=dimension_id)

        if form.is_valid():
            question = form.save(commit=False)
            question.survey = self.survey
            question.type_field = self.type_field_id
            question.save()
            self.object = question
            messages.success(request, gettext("%(page_action_name)s succeeded.") % {'page_action_name': capfirst(self.title_page.lower())})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'object' not in context:
            context['object'] = None
        context['type_field_id'] = self.type_field_id
        return context

    def get_success_url(self):
        return reverse("djf_surveys:admin_forms_survey", args=[self.survey.slug])

    def get_sub_title_page(self):
        return gettext("Type Field %s") % Question.TYPE_FIELD[self.type_field_id][1]

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminUpdateQuestionView(ContextTitleMixin, UpdateView):
    model = Question
    template_name = 'djf_surveys/admins/question_form.html'
    success_url = reverse_lazy("djf_surveys:")
    title_page = _("Edit Question")
    survey = None
    type_field_id = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.type_field_id = self.object.type_field
        self.survey = self.object.survey
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        choices = [TYPE_FIELD.multi_select, TYPE_FIELD.select, TYPE_FIELD.radio]
        if self.type_field_id in choices:
            return QuestionWithChoicesForm
        else:
            return QuestionForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if 'dimension' in request.POST:
            dimension_id = request.POST.get('dimension')
            form.fields['subdimension'].queryset = SubDimension.objects.filter(dimension__id=dimension_id)

        if form.is_valid():
            self.object = form.save()
            messages.success(request, gettext("%(page_action_name)s succeeded.") % {'page_action_name': capfirst(self.title_page.lower())})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'object' not in context:
            context['object'] = None
        context['type_field_id'] = self.type_field_id
        return context

    def get_success_url(self):
        return reverse("djf_surveys:admin_forms_survey", args=[self.survey.slug])

    def get_sub_title_page(self):
        return gettext("Type Field %s") % self.object.get_type_field_display()


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminDeleteQuestionView(DetailView):
    model = Question
    survey = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        messages.success(request, gettext("Question %ss succesfully deleted.") % question.label)
        return redirect("djf_surveys:admin_forms_survey", slug=self.survey.slug)


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class AdminChangeOrderQuestionView(View):
    def post(self, request, *args, **kwargs):
        ordering = request.POST['order_question'].split(",")
        for index, question_id in enumerate(ordering):
            if question_id:
                question = Question.objects.get(id=question_id)
                question.ordering = index
                question.save()

        data = {
            'message': gettext("Update ordering of questions succeeded.")
        }
        return JsonResponse(data, status=200)


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class DownloadResponseSurveyView(DetailView):
    model = Survey

    def get(self, request, *args, **kwargs):
        survey = self.get_object()
        user_answers = UserAnswer.objects.filter(survey=survey)
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        rows = []
        header = []
        for index, user_answer in enumerate(user_answers):
            if index == 0:
                header.append('user')
                header.append('update_at')

            rows.append(user_answer.user.username if user_answer.user else 'no auth')
            rows.append(user_answer.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
            for answer in user_answer.answer_set.all():
                if index == 0:
                    header.append(answer.question.label)
                rows.append(answer.get_value_for_csv)

            if index == 0:
                writer.writerow(header)
            writer.writerow(rows)
            rows = []

        response = HttpResponse(csv_buffer.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename={survey.slug}.csv'
        return response


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Orchestrator','Supervisor'])], name='dispatch')
class SummaryResponseSurveyView(DetailView):
    model = Survey
    template_name = "djf_surveys/admins/summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        context['dimensions'] = Dimension.objects.filter(questions__survey=survey).distinct()
        context['subdimensions'] = SubDimension.objects.filter(dimension__questions__survey=survey).distinct()

        dimension_id = self.request.GET.get('dimension')
        subdimension_id = self.request.GET.get('subdimension')
        
        summary = SummaryResponse(survey=survey)
        context['full_summary'] = summary.generate()

        if subdimension_id:
            context['selected_subdimension'] = subdimension_id
            context['summary_content'] = summary.generate(subdimension_id=subdimension_id)
        elif dimension_id:
            context['selected_dimension'] = dimension_id
            context['summary_content'] = summary.generate(dimension_id=dimension_id)
        else:
            context['summary_content'] = summary.generate()

        return context