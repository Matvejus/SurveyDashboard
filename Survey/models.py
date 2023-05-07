from django.db import models
import datetime

# Models for Survey


class SurveyStatus(models.Model):
    survey_status_id = models.AutoField(primary_key=True)
    survey_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.survey_status}"


class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_name = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    min_responses = models.IntegerField(blank=True, null=True)
    max_responses = models.IntegerField(blank=True, null=True)
    survey_status = models.ForeignKey("SurveyStatus", models.DO_NOTHING)

    def __str__(self):
        return f"{self.survey_name}"


class QuestionType(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.question_type}"


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_order = models.IntegerField(blank=True, null=True)
    question_text = models.CharField(max_length=2000, blank=True, null=True)
    is_mandatory = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    question_type = models.ForeignKey("QuestionType", models.DO_NOTHING)

    def __str__(self):
        return f"{self.question_text}"


class QuestionOption(models.Model):
    question_option_id = models.AutoField(primary_key=True)
    qo_order = models.IntegerField(
        db_column="QO_order", blank=True, null=True
    )  # Field name made lowercase.
    qo_value = models.CharField(
        db_column="QO_value", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    question = models.ForeignKey(Question, models.DO_NOTHING)



class Respondent(models.Model):
    respondent_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Respondent"


class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    respondent = models.ForeignKey(Respondent, models.DO_NOTHING)
    survey = models.ForeignKey("Survey", models.DO_NOTHING)
    begin_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.survey} - {self.respondent}"


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    response = models.ForeignKey("Response", models.DO_NOTHING)
    question = models.ForeignKey("Question", models.DO_NOTHING)
    answer = models.CharField(max_length=6000, blank=True, null=True)

    def __str__(self):
        return f"{self.answer}"


class AnswerOption(models.Model):
    answer_option_id = models.AutoField(primary_key=True)
    answer = models.ForeignKey(Answer, models.DO_NOTHING)
    question_option = models.ForeignKey("QuestionOption", models.DO_NOTHING)
