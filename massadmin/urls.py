from django.urls import path
from .massadmin import mass_change_view


urlpatterns = [
    path(
        '<str:app_name>/<str:model_name>-masschange/<str:object_ids>/',
        mass_change_view,
        name='massadmin_change_view',
    ),
]
