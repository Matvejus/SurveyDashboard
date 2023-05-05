from django.contrib import admin
from .models import Survey, SurveyStatus, Question, QuestionType, QuestionOption, Respondent, Response, Answer

class SurveyStatusAdmin(admin.ModelAdmin):
    list_display = ['survey_status_id', 'survey_status']

admin.site.register(SurveyStatus, SurveyStatusAdmin)

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    inlines = [QuestionOptionInline]

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['survey_id', 'survey_name', 'description', 'start_date', 'end_date', 'min_responses', 'max_responses', 'survey_status']
    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)

class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['question_type_id', 'question_type']

admin.site.register(QuestionType, QuestionTypeAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'question_order', 'question_text', 'is_mandatory', 'question_type']

admin.site.register(Question, QuestionAdmin)

class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question_option_id', 'qo_order', 'qo_value', 'question']

admin.site.register(QuestionOption, QuestionOptionAdmin)

class RespondentAdmin(admin.ModelAdmin):
    list_display = ['respondent_id', 'first_name', 'last_name', 'email']

admin.site.register(Respondent, RespondentAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['response_id', 'respondent', 'survey', 'begin_date', 'end_date']

admin.site.register(Response, ResponseAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_id', 'response', 'question', 'answer']

admin.site.register(Answer, AnswerAdmin)
