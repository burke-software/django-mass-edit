# Updates by David Burke <david@burkesoftware.com>
# Orginal code is at
# http://algoholic.eu/django-mass-change-admin-site-extension/
"""
Copyright (c) 2010, Stanislaw Adaszewski
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Stanislaw Adaszewski nor the
      names of any contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Stanislaw Adaszewski BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import inspect

from django.contrib import admin
from django.conf.urls import patterns
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction, models
try:
    from django.contrib.admin.utils import unquote
except ImportError:
    from django.contrib.admin.util import unquote
from django.contrib.admin import helpers
from django.utils.translation import ugettext_lazy as _
import collections
try:
    from django.utils.encoding import force_text
except:  # 1.4 compat
    from django.utils.encoding import force_unicode as force_text
from django.utils.safestring import mark_safe
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import Http404, HttpResponseRedirect
from django.utils.html import escape
from django.contrib.contenttypes.models import ContentType
from django import template
from django.shortcuts import render_to_response
from django.forms.formsets import all_valid

import sys

urls = patterns(
    '',
    (r'(?P<app_name>[^/])/(?P<model_name>[^/]+)-masschange/(?P<object_ids>[0-9,]+)/$',
     'massadmin.massadmin.mass_change_view'),
)

# noinspection PyUnusedLocal


def mass_change_selected(modeladmin, request, queryset):
    selected_int = queryset.values_list('pk', flat=True)
    selected = []
    for s in selected_int:
        selected.append(str(s))
    return HttpResponseRedirect(
        '../%s-masschange/%s' %
        (modeladmin.model._meta.model_name, ','.join(selected)))
mass_change_selected.short_description = _('Mass Edit')


def mass_change_view(request, app_name, model_name, object_ids):
    model = models.get_model(app_name, model_name)
    ma = MassAdmin(model, admin.site)
    return ma.mass_change_view(request, object_ids)

# noinspection PyRedeclaration
mass_change_view = staff_member_required(mass_change_view)


class MassAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        try:
            self.admin_obj = admin_site._registry[model]
        except KeyError:
            raise Exception('Model not registered with the admin site.')

        for (varname, var) in self.get_overrided_properties().items():
            if not varname.startswith('_'):
                self.__dict__[varname] = var

        super(MassAdmin, self).__init__(model, admin_site)

    def get_overrided_properties(self):
        """
        Find all overrided properties, like form, raw_id_fields and so on.
        """
        items = {}
        for cl in inspect.getmro(self.admin_obj.__class__):
            if cl is admin.ModelAdmin:
                break
            for k, v in cl.__dict__.items():
                if not k in items:
                    items[k] = v
        return items

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta

        msg = _('Selected %(name)s were changed successfully.') % {
            'name': force_text(
                opts.verbose_name_plural),
            'obj': force_text(obj)}

        self.message_user(request, msg)
        preserved_filters = self.get_preserved_filters(request)
        redirect_url = reverse('admin:{}_{}_changelist'.format(
            self.model._meta.app_label,
            self.model._meta.model_name,
        ))
        redirect_url = add_preserved_filters(
            {'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
        return HttpResponseRedirect(redirect_url)

    def render_mass_change_form(
            self,
            request,
            context,
            add=False,
            change=False,
            form_url='',
            obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': mark_safe(form_url),
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
        })
        context_instance = template.RequestContext(
            request,
            current_app=self.admin_site.name)
        return render_to_response(
            self.change_form_template or [
                "admin/%s/%s/mass_change_form.html" %
                (app_label,
                 opts.object_name.lower()),
                "admin/%s/mass_change_form.html" %
                app_label,
                "admin/mass_change_form.html"],
            context,
            context_instance=context_instance)

    def mass_change_view(
            self,
            request,
            comma_separated_object_ids,
            extra_context=None):
        """The 'mass change' admin view for this model."""
        global new_object
        model = self.model
        opts = model._meta
        general_error = None

        # Allow model to hide some fields for mass admin
        exclude_fields = getattr(self.admin_obj, "massadmin_exclude", ())
        queryset = getattr(
            self.admin_obj,
            "massadmin_queryset",
            self.get_queryset)(request)

        object_ids = comma_separated_object_ids.split(',')
        object_id = object_ids[0]

        try:
            obj = queryset.get(pk=unquote(object_id))
        except model.DoesNotExist:
            obj = None

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': force_text(
                        opts.verbose_name),
                    'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        errors, errors_list = None, None
        mass_changes_fields = request.POST.getlist("_mass_change")
        if request.method == 'POST':
            # commit only when all forms are valid
            with transaction.atomic():
                try:
                    objects_count = 0
                    changed_count = 0
                    objects = queryset.filter(pk__in=object_ids)
                    for obj in objects:
                        objects_count += 1
                        form = ModelForm(
                            request.POST,
                            request.FILES,
                            instance=obj)

                        exclude = []
                        for fieldname, field in list(form.fields.items()):
                            if fieldname not in mass_changes_fields:
                                exclude.append(fieldname)

                        for exclude_fieldname in exclude:
                            del form.fields[exclude_fieldname]

                        if form.is_valid():
                            form_validated = True
                            new_object = self.save_form(
                                request,
                                form,
                                change=True)
                        else:
                            form_validated = False
                            new_object = obj
                        prefixes = {}
                        for FormSet in self.get_formsets(request, new_object):
                            prefix = FormSet.get_default_prefix()
                            prefixes[prefix] = prefixes.get(prefix, 0) + 1
                            if prefixes[prefix] != 1:
                                prefix = "%s-%s" % (prefix, prefixes[prefix])
                            if prefix in mass_changes_fields:
                                formset = FormSet(
                                    request.POST,
                                    request.FILES,
                                    instance=new_object,
                                    prefix=prefix)
                                formsets.append(formset)

                        if all_valid(formsets) and form_validated:
                            #self.admin_obj.save_model(request, new_object, form, change=True)
                            self.save_model(
                                request,
                                new_object,
                                form,
                                change=True)
                            form.save_m2m()
                            for formset in formsets:
                                self.save_formset(
                                    request,
                                    form,
                                    formset,
                                    change=True)

                            change_message = self.construct_change_message(
                                request,
                                form,
                                formsets)
                            self.log_change(
                                request,
                                new_object,
                                change_message)
                            changed_count += 1

                    if changed_count == objects_count:
                        return self.response_change(request, new_object)
                    else:
                        errors = form.errors
                        errors_list = helpers.AdminErrorList(form, formsets)

                finally:
                    general_error = sys.exc_info()[1]

        form = ModelForm(instance=obj)
        form._errors = errors
        prefixes = {}
        for FormSet in self.get_formsets(request, obj):
            prefix = FormSet.get_default_prefix()
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
            if prefixes[prefix] != 1:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset = FormSet(instance=obj, prefix=prefix)
            formsets.append(formset)

        adminForm = helpers.AdminForm(
            form, self.get_fieldsets(
                request, obj), self.prepopulated_fields, self.get_readonly_fields(
                request, obj), model_admin=self.admin_obj)
        media = self.media + adminForm.media

        # We don't want the user trying to mass change unique fields!
        unique_fields = []
        for field_name in model._meta.get_all_field_names():
            try:
                field = model._meta.get_field(field_name)
                if field.unique:
                    unique_fields.append(field_name)
            except:
                pass

        # Buggy! Use at your own risk
        #inline_admin_formsets = []
        # for inline, formset in zip(self.inline_instances, formsets):
        #    fieldsets = list(inline.get_fieldsets(request, obj))
        #    inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
        #    inline_admin_formsets.append(inline_admin_formset)
        #    media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_text(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'unique_fields': unique_fields,
            'exclude_fields': exclude_fields,
            'is_popup': '_popup' in request.REQUEST,
            'media': mark_safe(media),
            #'inline_admin_formsets': inline_admin_formsets,
            'errors': errors_list,
            'general_error': general_error,
            'app_label': opts.app_label,
            'object_ids': comma_separated_object_ids,
            'mass_changes_fields': mass_changes_fields,
        }
        context.update(extra_context or {})
        return self.render_mass_change_form(
            request,
            context,
            change=True,
            obj=obj)