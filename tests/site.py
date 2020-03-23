from django.contrib.admin.sites import AdminSite

class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['custom_variable'] = 'custom_value'
        return context
