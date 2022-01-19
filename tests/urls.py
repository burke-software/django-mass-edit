from django.urls import include, path
from django.contrib import admin
from massadmin import urls as massadmin_urls
admin.autodiscover()

urlpatterns = [
    path('admin/', include(massadmin_urls)),
    path('admin/', admin.site.urls),
]
