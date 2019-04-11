from django.conf.urls import url
from .massadmin import mass_change_view


urlpatterns = [
    url(r'(?P<app_name>[^/]+)/(?P<model_name>[^/]+)-masschange/(?P<object_ids>[\w,\.\-]+)/$',
     mass_change_view,
     name='massadmin_change_view'),
]
