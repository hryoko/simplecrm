from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customers'
    # verbose_name = 'こきゃく'
    verbose_name_plural = 'こきゃく'
