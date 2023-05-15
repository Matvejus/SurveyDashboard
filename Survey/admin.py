from django.contrib import admin
from Survey.models import (
    Organisation,
    SurveyStatus,
    Survey,
    QuestionType,
    Question,
    Choice,
    Submission,
    User,
)

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class ChoiceInline(admin.TabularInline):
    model = Choice


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_id", "question")


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("org_id", "organisation")


class SurveyStatusAdmin(admin.ModelAdmin):
    list_display = ("status_id", "status")


class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("status", "title", "description", "org")


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ("type_id", "text")


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("type", "survey", "pub_date")


class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "email", "org")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "submission_id",
        "user",
        "survey",
        "sub_date",
    )


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(SurveyStatus, SurveyStatusAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
