# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    response = models.ForeignKey("Response", models.DO_NOTHING)
    question = models.ForeignKey("Question", models.DO_NOTHING)
    answer = models.CharField(max_length=6000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Answer"


class AnswerOption(models.Model):
    answer_option_id = models.AutoField(primary_key=True)
    answer = models.ForeignKey(Answer, models.DO_NOTHING)
    question_option = models.ForeignKey("QuestionOption", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Answer_Option"


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_order = models.IntegerField(blank=True, null=True)
    question_text = models.CharField(max_length=2000, blank=True, null=True)
    is_mandatory = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    question_type = models.ForeignKey("QuestionType", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Question"


class QuestionOption(models.Model):
    question_option_id = models.AutoField(primary_key=True)
    qo_order = models.IntegerField(
        db_column="QO_order", blank=True, null=True
    )  # Field name made lowercase.
    qo_value = models.CharField(
        db_column="QO_value", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    question = models.ForeignKey(Question, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Question_Option"


class QuestionType(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Question_Type"


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

    class Meta:
        managed = False
        db_table = "Response"


class Survey(models.Model):
    survey_id = models.AutoField(primary_key=True)
    survey_name = models.CharField(max_length=100)
    description = models.CharField(max_length=8000)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    min_responses = models.IntegerField(blank=True, null=True)
    max_responses = models.IntegerField(blank=True, null=True)
    survey_status = models.ForeignKey("SurveyStatus", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "Survey"


class SurveyStatus(models.Model):
    survey_status_id = models.AutoField(primary_key=True)
    survey_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Survey_Status"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"
