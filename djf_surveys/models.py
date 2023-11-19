import random, string
from collections import namedtuple

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from djf_surveys import app_settings
from djf_surveys.utils import create_star




TYPE_FIELD = namedtuple(
    'TYPE_FIELD', 'text number radio select multi_select text_area url email date rating'
)._make(range(10))


def generate_unique_slug(klass, field, id, identifier='slug'):
    """
    Generate unique slug.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    mapping = {
        identifier: unique_slug,
    }
    obj = klass.objects.filter(**mapping).first()
    while obj:
        if obj.id == id:
            break
        rnd_string = random.choices(string.ascii_lowercase, k=(len(unique_slug)))
        unique_slug = '%s-%s-%d' % (origin_slug, ''.join(rnd_string[:10]), numb)
        mapping[identifier] = unique_slug
        numb += 1
        obj = klass.objects.filter(**mapping).first()
    return unique_slug

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_at']


class Survey(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), default='')
    slug = models.SlugField(_("slug"), max_length=225, default='')
    editable = models.BooleanField(_("editable"), default=True, help_text=_("If False, user can't edit record."))
    deletable = models.BooleanField(_("deletable"), default=True, help_text=_("If False, user can't delete record."))
    duplicate_entry = models.BooleanField(_("mutiple submissions"), default=False, help_text=_("If True, user can resubmit."))
    private_response = models.BooleanField(_("private response"), default=False, help_text=_("If True, only admin and owner can access."))
    can_anonymous_user = models.BooleanField(_("anonymous submission"), default=False, help_text=_("If True, user without authentatication can submit."))
    org_type = models.CharField(_("Organization type"), blank = True, max_length = 200)
    
    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = generate_unique_slug(Survey, self.slug, self.id)
        else:
            self.slug = generate_unique_slug(Survey, self.name, self.id)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

class Level(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.label


class Dimension(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.ManyToManyField(Level, related_name='dimensions')

    def __str__(self):
        return self.id


class SubDimension(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dimension = models.ManyToManyField(Dimension, related_name='sub_dimensions')

    def __str__(self):
        return self.id

class Question(BaseModel):
    TYPE_FIELD = [
        (TYPE_FIELD.text, _("Text")),
        (TYPE_FIELD.number, _("Number")),
        (TYPE_FIELD.radio, _("Radio")),
        (TYPE_FIELD.select, _("Select")),
        (TYPE_FIELD.multi_select, _("Multi Select")),
        (TYPE_FIELD.text_area, _("Text Area")),
        (TYPE_FIELD.url, _("URL")),
        (TYPE_FIELD.email, _("Email")),
        (TYPE_FIELD.date, _("Date")),
        (TYPE_FIELD.rating, _("Rating"))
    ]
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='questions')
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='questions')
    subdimension = models.ForeignKey(SubDimension, on_delete=models.CASCADE, related_name='questions')
    key = models.CharField(_("key"), max_length=225, unique=True, null=True, blank=True,
                           help_text=_("Unique key for this question, fill in the blank if you want to use for automatic generation."))
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name=_("survey"))
    label = models.CharField(_("label"), max_length=500, help_text=_("Enter your question in here."))
    type_field = models.PositiveSmallIntegerField(_("type of input field"), choices=TYPE_FIELD)
    choices = models.TextField(
        _("choices"),
        blank=True, null=True,
        help_text=_("If type of field is radio, select, or multi select, fill in the options separated by commas. Ex: Male, Female.")
    )
    help_text = models.CharField(
        _("help text"),
        max_length=200, blank=True, null=True,
        help_text=_("You can add a help text in here.")
    )
    required = models.BooleanField(_("required"), default=True, help_text=_("If True, the user must provide an answer to this question."))
    ordering = models.PositiveIntegerField(_("choices"), default=0, help_text=_("Defines the question order within the surveys."))

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ["ordering"]    

    def __str__(self):
        return f"{self.label}-survey-{self.survey.id}"

    def save(self, *args, **kwargs):
        if self.key:
            self.key = generate_unique_slug(Question, self.key, self.id, "key")
        else:
            self.key = generate_unique_slug(Question, self.label, self.id, "key")
            
        super(Question, self).save(*args, **kwargs)


class UserAnswer(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"))
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("user"))
    
    class Meta:
        verbose_name = _("user answer")
        verbose_name_plural = _("user answers")
        ordering = ["-updated_at"]

    def __str__(self):
        return str(self.id)

    def get_user_photo(self):
        default_photo = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSmiley&psig=AOvVaw37yL7OOD0qcGmTVkbRk7Hx&ust=1686701802745000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCMjQxYD8vv8CFQAAAAAdAAAAABAE"
        if app_settings.SURVEY_USER_PHOTO_PROFILE:
            try:
                return eval(app_settings.SURVEY_USER_PHOTO_PROFILE)
            except:
                return default_photo
        return default_photo


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, verbose_name=_("question"))
    value = models.TextField(_("value"), help_text=_("The value of the answer given by the user."))
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE, verbose_name=_("user answer"))

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")
        ordering = ["question__ordering"]

    def __str__(self):
        return f"{self.question}: {self.value}"

    @property
    def get_value(self):
        if self.question.type_field == TYPE_FIELD.rating:
            return create_star(active_star=int(self.value))
        elif self.question.type_field == TYPE_FIELD.url:
            return mark_safe(f'<a href="{self.value}" target="_blank">{self.value}</a>')
        elif self.question.type_field == TYPE_FIELD.radio or self.question.type_field == TYPE_FIELD.select or\
                self.question.type_field == TYPE_FIELD.multi_select:
            return self.value.strip().replace("_", " ").capitalize()
        else:
            return self.value
    
    @property
    def get_value_for_csv(self):
        if self.question.type_field == TYPE_FIELD.radio or self.question.type_field == TYPE_FIELD.select or\
                self.question.type_field == TYPE_FIELD.multi_select:
            return self.value.strip().replace("_", " ").capitalize()
        else:
            return self.value.strip()
