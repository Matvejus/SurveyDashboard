from typing import List, Tuple

from django import forms
from django.db.models.base import Model
from organization.models import OrgProfile
from .models import Survey
from django.db import transaction
from django.core.validators import MaxLengthValidator
from django.forms.models import modelform_factory


from django.utils.translation import gettext_lazy as _
from djf_surveys.models import Answer, TYPE_FIELD, UserAnswer, Question, Level, Dimension, SubDimension, EditField
from djf_surveys.widgets import CheckboxSelectMultipleSurvey, RadioSelectSurvey, DateSurvey, RatingSurvey, InlineChoiceField, InlineEditFieldsWidget
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

    class Meta:
        model = Survey
        fields = [
            'name', 'description', 'collaboration_network', 'org_type', 'editable', 'deletable',
            'duplicate_entry', 'private_response', 'can_anonymous_user',
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
            self.add_edit_fields(user)

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
    edit_field = forms.CharField(
        widget=InlineEditFieldsWidget(attrs={'class': 'w-full p-4 pr-12 text-sm border-gray-500 rounded-lg shadow-sm'}, extra=3),
        required=False,
        label="Edit Fields",
    )

    class Meta:
        model = Question
        fields = ['label', 'edit_field', 'key', 'level', 'dimension', 'subdimension', 'help_text', 'required']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['subdimension'].queryset = SubDimension.objects.none()

        if 'dimension' in self.data:
            try:
                dimension_id = int(self.data.get('dimension'))
                self.fields['subdimension'].queryset = SubDimension.objects.filter(dimension_id=dimension_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty SubDimension queryset
        elif self.instance.pk:
            self.fields['subdimension'].queryset = self.instance.dimension.sub_dimensions.order_by('id')
        
    def save(self, commit=True):
        instance = super(QuestionForm, self).save(commit=False)
        edit_field_data = self.cleaned_data.get('edit_field')

        # Example logic for handling edit_field_data
        # You would need to adjust this logic based on your actual requirements
        if edit_field_data:
            # Here you might need to parse edit_field_data, find or create an EditField instance
            # For demonstration purposes, let's say we create a new EditField instance
            edit_field_instance, created = EditField.objects.get_or_create(options=edit_field_data)
            instance.edit_field = edit_field_instance

        if commit:
            instance.save()
            self.save_m2m()  # In case there are many-to-many fields to save

        return instance
    
    

class QuestionWithChoicesForm(forms.ModelForm):
    edit_field = forms.CharField(
        widget=InlineEditFieldsWidget(attrs={'class': 'w-full p-4 pr-12 text-sm border-gray-500 rounded-lg shadow-sm'}, extra=3),
        required=False,
        label="Edit Fields",
    )

    class Meta:
        model = Question
        fields = ('label', 'edit_field', 'key', 'level', 'dimension', 'subdimension', 'choices', 'help_text', 'required')

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
    


class SelectQuestionsForm(forms.ModelForm):

    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), 
                                    widget = CheckboxSelectMultipleSurvey())

    class Meta:
        model = Survey
        fields = ['questions']



def create_question_form(questions):
    
    fields = {}
    for question in questions:
        field_name = f"question_{question.id}"
        fields[field_name] = forms.ModelMultipleChoiceField(
            queryset=Question.objects.filter(id=question.id),
            required=False,
            widget= CheckboxSelectMultipleSurvey,
            label=question.label,
        )

    # Create the form class using modelform_factory
    QuestionForm = type('QuestionForm', (forms.Form,), fields)
    return QuestionForm

def save_survey_from_form(survey, form_data):
    question_ids = [int(value[0]) for key, value in form_data.items() if key.startswith('question_')]
    selected_questions = Question.objects.filter(id__in=question_ids)

    # Log the selected question IDs for debugging
    print(f"Selected Question IDs: {question_ids}")

    for question in selected_questions:
        survey.questions.add(question)
        # Log each question being added to the survey

    # Save the survey object
    survey.save()
    print(f"Survey '{survey.name}' saved with updated questions: {survey.questions.all()}")

class EditFieldForm(forms.ModelForm):
    class Meta:
        model = EditField
        fields = ['options']