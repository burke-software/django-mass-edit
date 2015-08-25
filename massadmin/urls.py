from django.conf.urls import url, patterns


urlpatterns = patterns('',
    url(r'(?P<app_name>[^/]+)/(?P<model_name>[^/]+)-masschange/(?P<object_ids>[\w,\.]+)/$',
     'massadmin.massadmin.mass_change_view',
     name='massadmin_change_view'),
)
