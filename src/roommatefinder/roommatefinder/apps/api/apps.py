from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiAppConfig(AppConfig):
    name = 'roommatefinder.apps.api'
    verbose_name = _("api") # human readable