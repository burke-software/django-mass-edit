from django.conf.urls import *

urlpatterns = patterns('',
    (r'(?P<app_name>[^/]+)/(?P<model_name>[^/]+)-masschange/(?P<object_ids>[0-9,]+)$',
     'massadmin.massadmin.mass_change_view'),
)
