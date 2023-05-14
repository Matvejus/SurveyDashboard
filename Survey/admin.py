from django.contrib import admin
from .models import Survey, QuestionType, Question, QuestionOption, Respondent, Response, Answer, AnswerOption
from organization.models import OrgProfile

# to have multiple questions in a survey
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Number of empty "extra" forms

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'survey_name', 'description', 'start_date', 'end_date', 'survey_status', 'org_profiles_list']
    inlines = [QuestionInline]
    filter_horizontal = ['org_profiles']

    def org_profiles_list(self, obj):
        return ", ".join([str(profile) for profile in obj.org_profiles.all()])

    org_profiles_list.short_description = 'Related OrgProfiles'

admin.site.register(Survey, SurveyAdmin)

class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']

admin.site.register(QuestionType, QuestionTypeAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'survey', 'question_text', 'is_mandatory', 'question_type']

admin.site.register(Question, QuestionAdmin)

class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'option_text']

admin.site.register(QuestionOption, QuestionOptionAdmin)

class RespondentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_first_name', 'get_last_name', 'get_email', 'get_organization_name']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'  #Renames column head

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_organization_name(self, obj):
        return obj.organization.title  # assuming the field name is 'title' in 'OrgProfile' model
    get_organization_name.short_description = 'Organization Name'

admin.site.register(Respondent, RespondentAdmin)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'respondent', 'survey']

admin.site.register(Response, ResponseAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'response', 'question', 'answer']

admin.site.register(Answer, AnswerAdmin)

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'question_option']

admin.site.register(AnswerOption, AnswerOptionAdmin)
