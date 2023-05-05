# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_name = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    min_responses = models.IntegerField(blank=True, null=True)
    max_responses = models.IntegerField(blank=True, null=True)
    survey_status = models.ForeignKey("SurveyStatus", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Survey"

class SurveyStatus(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Finished', 'Finished'),
        ('Unstarted', 'Unstarted'),
    ]

    survey_status_id = models.AutoField(primary_key=True)
    survey_status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    class Meta:
        db_table = "SurveyStatus"

    def __str__(self):
        return self.survey_status

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)  # Added relationship to Survey
    question_order = models.IntegerField(blank=True, null=True)
    question_text = models.CharField(max_length=2000, blank=True, null=True)
    is_mandatory = models.BooleanField(default=False)
    question_type = models.ForeignKey("QuestionType", models.DO_NOTHING)

    class Meta:
        db_table = "Question"

class QuestionType(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Question_Type"

class QuestionOption(models.Model):
    question_option_id = models.AutoField(primary_key=True)
    qo_order = models.IntegerField(db_column="QO_order", blank=True, null=True)
    qo_value = models.CharField(db_column="QO_value", max_length=100, blank=True, null=True)
    question = models.ForeignKey("Question", models.DO_NOTHING)

    class Meta:
        db_table = "Question_Option"

class Respondent(models.Model):
    respondent_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Respondent"

class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    respondent = models.ForeignKey("Respondent", models.DO_NOTHING)
    survey = models.ForeignKey("Survey", models.DO_NOTHING)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "Response"

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    response = models.ForeignKey("Response", models.DO_NOTHING, default='')
    question = models.ForeignKey("Question", models.DO_NOTHING, default='')
    answer = models.CharField(max_length=6000, blank=True, null=True)
    question_option = models.ForeignKey("QuestionOption", models.DO_NOTHING, blank=True, null=True) # Added relationship to QuestionOption

    class Meta:
        db_table = "Answer"
