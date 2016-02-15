from django.conf.urls import include, url
from django.contrib import admin
from massadmin import urls as massadmin_urls
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(massadmin_urls)),
]
