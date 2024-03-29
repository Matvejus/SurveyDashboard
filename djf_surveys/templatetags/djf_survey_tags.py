from django.template import Library
from django.contrib.auth.models import Group
from djf_surveys.utils import create_star as utils_create_star
register = Library()


@register.filter(name='addclass')
def addclass(field, class_attr):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': class_attr})
    else:
        return field


@register.filter(name='get_id_field')
def get_id_field(field):
    parse = field.auto_id.split("_")
    return parse[-1]


@register.filter(name='create_star')
def create_star(number, args):
    return utils_create_star(active_star=int(number), id_element=args)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()