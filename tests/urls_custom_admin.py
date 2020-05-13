"""
Used in tests.tests.test_custom_admin_site_update
Make sure the package works with a custom admin on top of a regular admin
"""
from django.conf.urls import include, url
from django.contrib import admin
from massadmin import urls as massadmin_urls
from .admin import custom_admin_site
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^custom_admin_path/', custom_admin_site.urls),
    url(r'^custom_admin_path/', include(massadmin_urls), kwargs={'admin_site': custom_admin_site}),
]
