from django import forms


class CheckboxSelectMultipleSurvey(forms.CheckboxSelectMultiple):
    option_template_name = 'djf_surveys/widgets/checkbox_option.html'


class RadioSelectSurvey(forms.RadioSelect):
    option_template_name = 'djf_surveys/widgets/radio_option.html'


class DateSurvey(forms.DateTimeInput):
    template_name = 'djf_surveys/widgets/datepicker.html'


class RatingSurvey(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/star_rating.html'


class InlineEditFieldsWidget(forms.Widget):
    template_name = 'djf_surveys/widgets/inline_choices.html'
    extra = 3

    def __init__(self, attrs=None, extra=3, field_type='edit'):
        super().__init__(attrs)
        self.extra = extra
        self.field_type = field_type

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['field_type'] = self.field_type
        if value:
            context['widget']['values'] = [x.strip() for x in value.split(',')]
        else:
            context['widget']['values'] = []
        values_count = len(context['widget']['values'])
        context['widget']['extra'] = range(1 + values_count, self.extra + 1 + values_count)
        return context

class InlineChoiceField(forms.Widget):
    template_name = 'djf_surveys/widgets/inline_choices.html'
    extra = 3

    def __init__(self, attrs=None, extra=3, field_type='choice'):
        super().__init__(attrs)
        self.extra = extra
        self.field_type = field_type

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['field_type'] = self.field_type
        if value:
            context['widget']['values'] = [x.strip() for x in value.split(',')]
        else:
            context['widget']['values'] = []
        choices_count = len(context['widget']['values'])
        context['widget']['extra'] = range(1 + choices_count, self.extra + 1 + choices_count)
        return context