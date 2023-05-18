from django.db import models
from users.models import CustomUser
from organization.models import OrgProfile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Assuming CustomUser is your user model
""" CustomUser = get_user_model() idk what it is"""

#Main connector, 
class Survey(models.Model):
    SURVEY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('finished', 'Finished'),
        ('unstarted', 'Unstarted'),
    ]
    survey_name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9_]*$',
                'Only letters, numbers, and underscores are allowed.'
            ),
        ]
    )
    survey_name_slug = models.SlugField(max_length=100, unique=True, editable=False)
    description = models.CharField(max_length=8000)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    survey_status = models.CharField(max_length=10, choices=SURVEY_STATUS_CHOICES, default='unstarted')
    org_profiles = models.ManyToManyField('organization.OrgProfile', blank=True)

    def __str__(self):
        return self.survey_name
        

    def save(self, *args, **kwargs):
        self.survey_name_slug = slugify(self.survey_name)
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Survey)
def update_survey_status(sender, instance, **kwargs):
    if instance.end_date and instance.end_date < timezone.now():
        instance.survey_status = 'finished'


class Respondent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrgProfile, on_delete=models.CASCADE)


class Response(models.Model):
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(auto_now_add=True)

    @property
    def completion_time(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None



class Question(models.Model):

    TYPE_CHOICES = [
        ('checkbox', 'Multiple Choice'),
        ('radio', 'Single Choice'),
        ('range', 'Slider'),
    ]

    question_id = models.AutoField(primary_key=True)
    question_order = models.IntegerField(unique = True, blank=True, null=True)
    question_text = models.CharField(max_length=2000, blank=True, null=True)
    is_mandatory = models.BooleanField(default=False)
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    survey = models.ForeignKey("Survey", on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    


class QuestionOption(models.Model):#to store options for answers: are you satisfied? YES/NO
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=2000)

    def __str__(self):
        return self.option_text


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrgProfile, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

class AnswerOption(models.Model):#??? looks like it just duplicate the annswer and question option
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)  # For Multiple Choice, Checkbox and Drop Down answers

    def __str__(self):
        return self.question_option.option_text