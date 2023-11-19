from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Survey, Question, Answer, UserAnswer, Level, Dimension, SubDimension


from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.db.models import Count
from .models import Survey, Question, Answer, UserAnswer, Level, Dimension, SubDimension


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('question', 'value', 'user_answer')
    extra = 0
    readonly_fields = ('question', 'value_display')
    can_delete = False

    def value_display(self, obj):
        return format_html('<span style="white-space: pre-wrap;">{}</span>', obj.get_value)
    value_display.short_description = 'Value'


class QuestionInline(admin.StackedInline):
    model = Question
    fields = ('level', 'dimension', 'subdimension', 'key', 'label', 'type_field', 'choices', 'help_text', 'required', 'ordering')
    extra = 0


@admin.register(Survey)
class AdminSurvey(admin.ModelAdmin):
    list_display = ('name', 'slug', 'question_count', 'editable', 'deletable', 'duplicate_entry', 'private_response', 'can_anonymous_user')
    search_fields = ('name', 'description')
    inlines = [QuestionInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(question_count=Count('questions'))

    def question_count(self, obj):
        return obj.question_count
    question_count.admin_order_field = 'question_count'

    # Custom view to export survey data
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/<int:survey_id>/', self.admin_site.admin_view(self.export_survey), name='export-survey'),
        ]
        return custom_urls + urls

    def export_survey(self, request, survey_id):
        # Implement your export logic here
        # This is just a placeholder for the redirect
        self.message_user(request, "Export is not implemented yet.", level='warning')
        return HttpResponseRedirect("../")

    def export_survey_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(f'export/{selected[0]}/')

    export_survey_action.short_description = "Export selected survey to CSV"

    actions = [export_survey_action]


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    list_display = ('label', 'survey', 'type_field', 'required', 'ordering')
    list_filter = ('survey', 'type_field', 'required', 'level', 'dimension', 'subdimension')
    search_fields = ('label', 'help_text')
    inlines = [AnswerInline]
    actions = ['duplicate_questions']

    def duplicate_questions(self, request, queryset):
        for question in queryset:
            question.pk = None
            question.label = f'Copy of {question.label}'
            question.save()
    duplicate_questions.short_description = "Duplicate selected questions"


@admin.register(Answer)
class AdminAnswer(admin.ModelAdmin):
    list_display = ('question', 'value_display', 'user_answer')
    search_fields = ('value', 'question__label')
    list_filter = ('question__survey', 'question__level', 'question__dimension', 'question__subdimension')
    readonly_fields = ('question', 'value_display', 'user_answer')

    def value_display(self, obj):
        return format_html('<span style="white-space: pre-wrap;">{}</span>', obj.get_value)
    value_display.short_description = 'Value'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(UserAnswer)
class AdminUserAnswer(admin.ModelAdmin):
    list_display = ('survey', 'user', 'created_at', 'updated_at', 'user_photo')
    list_filter = ('survey', 'user', 'created_at')
    search_fields = ('survey__name', 'user__username')

    def user_photo(self, obj):
        return format_html('<img src="{}" width="30" height="30" style="border-radius: 50%;"/>', obj.get_user_photo())
    user_photo.short_description = 'User Photo'


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'dimension_count')
    search_fields = ('id', 'label', 'description')
    actions = ['duplicate_levels']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_dimension_count=Count('dimensions', distinct=True))

    def dimension_count(self, obj):
        return obj._dimension_count
    dimension_count.admin_order_field = '_dimension_count'
    dimension_count.short_description = 'Number of Dimensions'

    def duplicate_levels(self, request, queryset):
        for level in queryset:
            level.pk = None  # Clear the primary key to create a new object
            level.label = f'Copy of {level.label}'
            level.save()
    duplicate_levels.short_description = "Duplicate selected levels"

@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'get_levels', 'subdimension_count')
    search_fields = ('id', 'label', 'description')
    actions = ['duplicate_dimensions']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_subdimension_count=Count('sub_dimensions', distinct=True))

    def get_levels(self, obj):
        return ", ".join([level.label for level in obj.levels.all()])
    get_levels.short_description = 'Levels'

    def subdimension_count(self, obj):
        return obj._subdimension_count
    subdimension_count.admin_order_field = '_subdimension_count'
    subdimension_count.short_description = 'Number of SubDimensions'

    def duplicate_dimensions(self, request, queryset):
        for dimension in queryset:
            dimension.pk = None  # Clear the primary key to create a new object
            dimension.label = f'Copy of {dimension.label}'
            dimension.save()
    duplicate_dimensions.short_description = "Duplicate selected dimensions"

@admin.register(SubDimension)
class SubDimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'get_dimensions')
    search_fields = ('id', 'label', 'description')
    actions = ['duplicate_subdimensions']

    def get_dimensions(self, obj):
        return ", ".join([dimension.label for dimension in obj.dimensions.all()])
    get_dimensions.short_description = 'Dimensions'

    def duplicate_subdimensions(self, request, queryset):
        for subdimension in queryset:
            subdimension.pk = None  # Clear the primary key to create a new object
            subdimension.label = f'Copy of {subdimension.label}'
            subdimension.save()
    duplicate_subdimensions.short_description = "Duplicate selected subdimensions"