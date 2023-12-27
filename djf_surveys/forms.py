from typing import List, Tuple

from django import forms
from django.db.models.base import Model
from organization.models import OrgProfile
from .models import Survey
from django.db import transaction
from django.core.validators import MaxLengthValidator
from django.forms.models import modelform_factory


from django.utils.translation import gettext_lazy as _
from djf_surveys.models import Answer, TYPE_FIELD, UserAnswer, Question, Level, Dimension, SubDimension
from djf_surveys.widgets import CheckboxSelectMultipleSurvey, RadioSelectSurvey, DateSurvey, RatingSurvey, InlineChoiceField
from djf_surveys.app_settings import DATE_INPUT_FORMAT, SURVEY_FIELD_VALIDATORS
from djf_surveys.validators import validate_rating


def make_choices(question: Question) -> List[Tuple[str, str]]:
    choices = []
    for choice in question.choices.split(','):
        choice = choice.strip()
        choices.append((choice.replace(' ', '_').lower(), choice))
    return choices


class SurveyForm(forms.ModelForm):

    CHOICES = (("GVR_F", "Government - Federal or state government"),
               ("GVR_L", "Government - Local agency"),
               ("NGO", "NGO - National or International"),
               ("PRIV_MULTI", "Private sector - Multinational Corporation"),
               ("PRIV_NATIONAL", "Private sector - National Corporation"),
               ("SMALLHOLDER", "Smallholder producer"),
               ("PRODUCER", "Producer organization"),
               ("FARMERS_ASC", "Farmers' association"),
               ("LABOR_UNION", "Labor union"),
               ("OTHER", "Other civil society organization"),
           )
   
    org_type = forms.MultipleChoiceField(choices=CHOICES, widget = CheckboxSelectMultipleSurvey())
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), widget = CheckboxSelectMultipleSurvey())

    class Meta:
        model = Survey
        fields = [
            'name', 'description', 'collaboration_network', 'org_type', 'editable', 'deletable',
            'duplicate_entry', 'private_response', 'can_anonymous_user', 'questions',
        ]
     

class BaseSurveyForm(forms.Form):

    def __init__(self, survey, user, *args, **kwargs):
        self.survey = survey
        self.user = user if user.is_authenticated else None
        self.field_names = []
        self.questions = self.survey.questions.all().order_by('ordering')
        super().__init__(*args, **kwargs)

        for question in self.questions:
            # to generate field name
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                choices = make_choices(question)
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices, label=question.label,
                    widget=CheckboxSelectMultipleSurvey,
                )
            elif question.type_field == TYPE_FIELD.radio:
                choices = make_choices(question)
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices, label=question.label,
                    widget=RadioSelectSurvey
                )
            elif question.type_field == TYPE_FIELD.select:
                choices = make_choices(question)
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices, label=question.label
                )
            elif question.type_field == TYPE_FIELD.number:
                self.fields[field_name] = forms.IntegerField(label=question.label)
            elif question.type_field == TYPE_FIELD.url:
                self.fields[field_name] = forms.URLField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['url'])]
                )
            elif question.type_field == TYPE_FIELD.email:
                self.fields[field_name] = forms.EmailField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['email'])]
                )
            elif question.type_field == TYPE_FIELD.date:
                self.fields[field_name] = forms.DateField(
                    label=question.label, widget=DateSurvey(),
                    input_formats=DATE_INPUT_FORMAT
                )
            elif question.type_field == TYPE_FIELD.text_area:
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=forms.Textarea
                )
            elif question.type_field == TYPE_FIELD.rating:
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=RatingSurvey,
                    validators=[MaxLengthValidator(1), validate_rating]
                )
            else:
                self.fields[field_name] = forms.CharField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['text'])]
                )

            self.fields[field_name].required = question.required
            self.fields[field_name].help_text = question.help_text
            self.field_names.append(field_name)

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.field_names:
            try:
                field = cleaned_data[field_name]
            except KeyError:
                raise forms.ValidationError("You must enter valid data")

            if self.fields[field_name].required and not field:
                self.add_error(field_name, 'This field is required')

        return cleaned_data


class CreateSurveyForm(BaseSurveyForm):

    @transaction.atomic
    def save(self):
        cleaned_data = super().clean()

        user_answer = UserAnswer.objects.create(
            survey=self.survey, user=self.user
        )
        for question in self.questions:
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                value = ",".join(cleaned_data[field_name])
            else:
                value = cleaned_data[field_name]

            Answer.objects.create(
                question=question, value=value, user_answer=user_answer
            )


class EditSurveyForm(BaseSurveyForm):

    def __init__(self, user_answer, *args, **kwargs):
        self.survey = user_answer.survey
        self.user_answer = user_answer
        super().__init__(survey=self.survey, user=user_answer.user, *args, **kwargs)
        self._set_initial_data()

    def _set_initial_data(self):
        answers = self.user_answer.answer_set.all()

        for answer in answers:
            field_name = f'field_survey_{answer.question.id}'
            if answer.question.type_field == TYPE_FIELD.multi_select:
                self.fields[field_name].initial = answer.value.split(',')
            else:
                self.fields[field_name].initial = answer.value

    @transaction.atomic
    def save(self):
        cleaned_data = super().clean()
        self.user_answer.survey = self.survey
        self.user_answer.user = self.user
        self.user_answer.save()

        for question in self.questions:
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                value = ",".join(cleaned_data[field_name])
            else:
                value = cleaned_data[field_name]

            answer, created = Answer.objects.get_or_create(
                question=question, user_answer=self.user_answer,
                defaults={'question_id': question.id, 'user_answer_id': self.user_answer.id}
            )

            if not created and answer:
                answer.value = value
                answer.save()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('label', 'key', 'level', 'dimension', 'subdimension', 'help_text', 'required')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subdimension'].queryset = SubDimension.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        if 'dimension' in cleaned_data:
            dimension_id = cleaned_data.get('dimension').id
            SubDimension.objects.filter(dimension=dimension_id).order_by('id')

        elif self.instance.pk:
            self.fields['subdimension'].queryset = self.instance.dimension.subdimension_set.order_by('id')
        return cleaned_data
    
class QuestionWithChoicesForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('label', 'key', 'level', 'dimension', 'subdimension', 'choices', 'help_text', 'required')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].widget = InlineChoiceField()
        self.fields['choices'].help_text = _("Click Button Add to adding choice")
        self.fields['subdimension'].queryset = SubDimension.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        if 'dimension' in cleaned_data:
            dimension_id = cleaned_data.get('dimension').id
            SubDimension.objects.filter(dimension=dimension_id).order_by('id')

        elif self.instance.pk:
            self.fields['subdimension'].queryset = self.instance.dimension.subdimension_set.order_by('id')
        return cleaned_data
    


class CustomQuestionList(forms.ModelChoiceField):

    def label_from_instance(self, question):
        return f"{question.level} {question.dimension} {question.label} {question.choices}" 


class SelectQuestionsForm(forms.ModelForm):

    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), 
                                    widget = CheckboxSelectMultipleSurvey())

    class Meta:
        model = Survey
        fields = ['questions']




def create_question_form(self):
    questions = Question.objects.all()  # Get all questions from the database

    fields = {}
    for question in questions:
        field_name = f"question_{question.id}"  # Generate unique field name for each question
        fields[field_name] = forms.ModelChoiceField(
            queryset=Question.objects.filter(id=question.id),
            widget=CheckboxSelectMultipleSurvey(),
            required=False,
            label=question.label,
        )  # Create a checkbox for each question

    # Create the form class using modelform_factory
    QuestionForm = modelform_factory(Question, fields=fields, form=forms.Form)
    QuestionForm.base_fields = fields

    # Set the questions for the form
    initial_questions = []  # Create an empty list to store selected questions
    for question in self.questions.all():
        initial_questions.append(question.pk)
    form = QuestionForm(initial=initial_questions)  # Initialize the form with the selected questions

    return form




