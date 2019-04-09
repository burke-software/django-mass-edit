from django.apps import AppConfig
from django.contrib import admin
from . import settings


class MassAdminConfig(AppConfig):
    name = 'massadmin'
    verbose_name = "Mass edit"

    def ready(self):
        from .massadmin import mass_change_selected

        if settings.ADD_ACTION_GLOBALLY:
            admin.site.add_action(mass_change_selected)
