from collections.abc import Iterable

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from ..persons.models import Person

# @login_required
# class HomeView(TemplateView):
#     template_name = 'core/home.html'


# def index(request):
#     return render(request, 'core/index.html')

# def dashboard(request):
#     return render(request, 'core/dashboard.html')


class ModelMetaInfoMixin:
    model = None

    def get_meta_all(self):
        meta = self.model._meta
        meta_all = []

        for attr in dir(meta):
            if attr.startswith('_'):
                continue
            val = getattr(meta, attr)
            if callable(val):
                continue

            if attr == 'verbose_name_plural':
                is_list = False
                val_to_use = val
            else:
                if isinstance(val, Iterable) and not isinstance(val, (str, bytes)):
                    val_to_use = list(val)
                    is_list = True
                else:
                    val_to_use = val
                    is_list = False

            meta_all.append(
                {
                    'name': attr,
                    'value': val_to_use,
                    'is_list': is_list,
                }
            )
        return meta_all


class ModelFieldsInfoMixin:
    model = None

    def get_fields_info(self):
        fields_info = []
        for field in self.model._meta.get_fields():
            if field.auto_created and not field.concrete:
                continue

            info = {
                'name': field.name,
                'verbose_name': field.verbose_name,
                'help_text': field.help_text,
                'is_relation': field.is_relation,
                'related_model_name': None,
                'related_model_app_label': None,
                'many_to_many': field.many_to_many,
                'many_to_one': getattr(field, 'many_to_one', False),
                'one_to_many': getattr(field, 'one_to_many', False),
                'one_to_one': getattr(field, 'one_to_one', False),
            }

            if field.related_model:
                info['related_model_name'] = field.related_model._meta.model_name
                info['related_model_app_label'] = field.related_model._meta.app_label

            fields_info.append(info)
        return fields_info


class HomeView(ListView, ModelMetaInfoMixin, ModelFieldsInfoMixin):
    model = Person
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_all'] = self.get_meta_all()
        context['fields_info'] = self.get_fields_info()
        return context
