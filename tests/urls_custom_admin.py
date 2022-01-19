"""
Used in tests.tests.test_custom_admin_site_update
Make sure the package works with a custom admin on top of a regular admin
"""
from django.urls import include, path
from django.contrib import admin
from massadmin import urls as massadmin_urls
from .admin import custom_admin_site
admin.autodiscover()

urlpatterns = [
    path('custom_admin_path/', include(massadmin_urls), kwargs={'admin_site': custom_admin_site}),
    path('custom_admin_path/', custom_admin_site.urls),
    path('admin/', admin.site.urls),
]
