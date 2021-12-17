# coding: utf-8
from django.contrib import admin
from django import forms

from .models import CustomAdminModel, CustomAdminModel2, InheritedAdminModel


class CustomAdminForm(forms.ModelForm):

    def clean_name(self):
        """ Fake cleaning for tests
        """
        name = self.cleaned_data.get("name")
        if (self.instance.pk
                and name == "invalid {}".format(self.instance.pk)):
            raise forms.ValidationError("Invalid model name")
        return name

    class Meta:
        fields = ("name", )
        model = CustomAdminModel


class InheritedAdminInline(admin.TabularInline):
    model = InheritedAdminModel


class CustomAdmin(admin.ModelAdmin):
    inlines = [InheritedAdminInline, ]
    model = CustomAdminModel
    form = CustomAdminForm


class CustomAdminWithCustomTemplate(admin.ModelAdmin):
    model = CustomAdminModel2
    form = CustomAdminForm
    change_form_template = "admin/change_form_template.html"


admin.site.register(CustomAdminModel, CustomAdmin)
admin.site.register(CustomAdminModel2, CustomAdminWithCustomTemplate)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("name", )


class InheritedAdmin(BaseAdmin):
    model = InheritedAdminModel
    raw_id_fields = ("fk_field", )


admin.site.register(InheritedAdminModel, InheritedAdmin)

custom_admin_site = admin.AdminSite(name='myadmin')
custom_admin_site.register(CustomAdminModel, CustomAdmin)
