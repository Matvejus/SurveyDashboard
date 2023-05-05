from django.contrib import admin
from .models import OrgProfile
from .models import SurveyStatus
from .models import Survey
from .models import QuestionType
from .models import Question
from .models import QuestionOption 
from .models import Respondent 
from .models import Response
from .models import Answer
from .models import AnswerOption


# Register your models here.

admin.site.register(OrgProfile)

class SurveyStatusAdmin(admin.ModelAdmin):
    list_display = ['survey_status_id', 'survey_status']

admin.site.register(SurveyStatus, SurveyStatusAdmin)

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['survey_id', 'survey_name','description', 'start_date','end_date','min_responses', 'max_responses', 'survey_status']

admin.site.register(Survey, SurveyAdmin) 

class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['question_type_id', 'question_type']

admin.site.register(QuestionType, QuestionTypeAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'question_order','question_text', 'is_mandatory', 'question_type']

admin.site.register(Question, QuestionAdmin)

class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question_option_id', 'qo_order','qo_value', 'question']

admin.site.register(QuestionOption, QuestionOptionAdmin)

class RespondentAdmin(admin.ModelAdmin):
    list_display = ['respondent_id', 'first_name','last_name', 'email']

admin.site.register(Respondent, RespondentAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['response_id','respondent', 'survey', 'begin_date', 'end_date']

admin.site.register(Response, ResponseAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_id', 'response','question', 'answer']

admin.site.register(Answer, AnswerAdmin)

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['answer_option_id', 'answer','question_option']

admin.site.register(AnswerOption, AnswerOptionAdmin)