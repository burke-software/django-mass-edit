"""Customized django admin helpers."""

from django.contrib.admin import helpers


class MassInlineAdminFormset(helpers.InlineAdminFormSet):
    """Mass `InlineAdminFormset`."""

    def __init__(self, inline, formset, fieldsets, prepopulated_fields=None,
                 readonly_fields=None, model_admin=None, has_add_permission=True,
                 has_change_permission=True, has_delete_permission=True,
                 has_view_permission=True):
        super().__init__(
            inline, formset, fieldsets, prepopulated_fields,
            readonly_fields, model_admin, has_add_permission,
            has_change_permission, has_delete_permission,
            has_view_permission
        )
                
        self.exclude_fields = getattr(self.opts, "massadmin_exclude", ())
        self.mass_changes_fields = []
