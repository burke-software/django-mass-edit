from django.urls import re_path
from .massadmin import mass_change_view


urlpatterns = [
    re_path(
        r'(?P<app_name>[^/]+)/(?P<model_name>[^/]+)-masschange/(?P<object_ids>[\w,\.\-]+)/$',
        mass_change_view,
        name='massadmin_change_view',
    ),
]
