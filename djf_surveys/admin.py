from django.contrib import admin
from django import forms
from .models import Survey, Question, Answer, UserAnswer, Level, Dimension, SubDimension, EditField

class EditFieldInline(admin.TabularInline):
    model = EditField  # Direct reference to EditField
    extra = 1
    
class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('label', 'type_field', 'required', 'ordering')
    list_filter = ('type_field', 'required')
    search_fields = ('label', 'help_text')
    inlines = [EditFieldInline, ]

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'editable', 'deletable', 'duplicate_entry', 'private_response', 'can_anonymous_user', 'org_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description')
    search_fields = ('label', 'description')

@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'list_levels')
    search_fields = ('label', 'description')
    def list_levels(self, obj):
        return ", ".join([level.label for level in obj.level.all()])
    list_levels.short_description = 'Levels'

@admin.register(SubDimension)
class SubDimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'description', 'list_dimensions')
    search_fields = ('label', 'description')
    def list_dimensions(self, obj):
        return ", ".join([dimension.label for dimension in obj.dimension.all()])
    list_dimensions.short_description = 'Dimensions'


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'created_at', 'updated_at')
    list_filter = ('survey', 'user')
    search_fields = ('survey__name', 'user__username')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'value_display', 'user_answer')
    search_fields = ('value', 'question__label')
    readonly_fields = ('value_display',)
    def value_display(self, obj):
        return obj.get_value_display()
    value_display.short_description = 'Value'
