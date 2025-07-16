from django import template

from ..utils.utility import format_phone_number, normalize_phone_number

register = template.Library()


@register.filter
def normalize_phone(value):
    return normalize_phone_number(value)


@register.filter
def format_phone(value):
    return format_phone_number(value)


# 使用例
# {% load core_filters %}
# 電話番号: {{person.phone_number | format_phone}}


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメーターの一部を置き換える"""
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()


@register.filter()
def display_checkmark(boolean):
    if boolean == True:
        return 'C:/Users/yoko0/OneDrive/smashProject/staticfiles/admin/img/icon-yes.svg'

    if boolean == False:
        return "{% static 'admin/img/icon-no.svg' %}"


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    modelformのverbose_name取得
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter
def int_format(int):
    return f'1{int:005}'
