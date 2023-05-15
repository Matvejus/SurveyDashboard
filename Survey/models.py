from django.db import models

# Create your models here.
# Step 1 - Define models


class Organisation(models.Model):
    org_id = models.AutoField(primary_key=True)
    organisation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Organisation"


class SurveyStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "Survey_Status"

    def __str__(self):
        return self.status


class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    status = models.ForeignKey("SurveyStatus", models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=8000)
    org = models.ForeignKey(Organisation, models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Survey"

    def __str__(self):
        return self.title


class QuestionType(models.Model):
    type_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "Question_Type"

    def __str__(self):
        return self.text


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    type = models.ForeignKey("QuestionType", models.DO_NOTHING)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    class Meta:
        managed = False
        db_table = "Question"

    def __str__(self):
        return self.text


class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "Choice"

    def __str__(self):
        return f"{self.question.text}:{self.text}"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    org = models.ForeignKey(Organisation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "User"
    


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    user = models.ForeignKey("User", models.DO_NOTHING)
    answer = models.ManyToManyField(Choice)
    sub_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Submission"
     


# Step 1a - Create migrations

# Step 1b - Run the migrations
