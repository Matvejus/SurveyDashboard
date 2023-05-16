from django import forms
from Survey.models import Submission, Choice

#Haley's form for survey
class SurveyForm(forms.Form):
    email = forms.EmailField()
    question_1 = forms.ChoiceField(widget=forms.RadioSelect, choices=())

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        del self.fields["question_1"]
        for question in survey.question_set.all():
            choices = [(choice.choice_id, choice.text)
                       for choice in question.choice_set.all()]
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                widget=forms.RadioSelect, choices=choices
            )
            self.fields[f"question_{question.id}"].label = question.text

    def save(self):
        data = self.cleaned_data
        submission = Submission(
            survey=self.survey, participant_email=data["email"])
        submission.save()
        for question in self.survey.question_set.all():
            choice = Choice.objects.get(pk=data[f"question_{question.id}"])
            submission.answer.add(choice)

        submission.save()
        return submission