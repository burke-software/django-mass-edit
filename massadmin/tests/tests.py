from django.contrib.auth.models import User
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import CustomAdminModel, InheritedAdminModel
from .admin import CustomAdminForm, BaseAdmin, InheritedAdmin
from massadmin.massadmin import MassAdmin


def get_massadmin_url(objects):
    if not hasattr(objects, "__iter__"):
        objects = [objects]
    opts = objects[0]._meta
    try:
        model_name = opts.model_name
    except AttributeError:
        model_name = opts.module_name
    return reverse("massadmin_change_view",
                   kwargs={"app_name": opts.app_label, "model_name": model_name,
                           "object_ids": ",".join(str(o.pk) for o in objects)})


def get_changelist_url(model):
    opts = model._meta
    try:
        model_name = opts.model_name
    except AttributeError:
        model_name = opts.module_name
    return reverse("admin:{}_{}_changelist".format(opts.app_label, model_name))


class AdminViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_massadmin_form_generation(self):
        response = self.client.get(get_massadmin_url(self.user))
        self.assertContains(response, 'First name')

    def test_update(self):
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 3)]

        response = self.client.post(get_massadmin_url(models),
                                    {"_mass_change": "name",
                                     "name": "new name"})
        self.assertRedirects(response, get_changelist_url(CustomAdminModel))
        new_names = CustomAdminModel.objects.order_by("pk").values_list("name", flat=True)
        # all models have changed
        self.assertEqual(list(new_names), ["new name"] * 3)

    def test_preserve_filters(self):
        """ Preserve filters which was choosed in lookup form
        """
        self.fail()

    def test_invalid_form(self):
        """ Save nothing if some forms are invalid
        """
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 3)]

        response = self.client.post(get_massadmin_url(models),
                                    {"_mass_change": "name",
                                     "name": "invalid {}".format(models[-1].pk)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errornote')
        new_names = CustomAdminModel.objects.order_by("pk").values_list("name", flat=True)
        # all models stay the same
        self.assertEqual(list(new_names), [m.name for m in models])


class CustomizationTestCase(TestCase):
    """ MassAdmin has all customized options from related ModelAdmin
    """

    def test_custom_from(self):
        """ If form is overrided in ModelAdmin, it should be overrided in
        MassAdmin too.
        """
        ma = MassAdmin(CustomAdminModel, admin.site)
        self.assertEqual(ma.form, CustomAdminForm)

    def test_inheritance(self):
        """ If modeladmin is inherited from another customized modeladmin,
        MassAdmin get overriding from all of them.
        """
        ma = MassAdmin(InheritedAdminModel, admin.site)
        self.assertEqual(ma.raw_id_fields, InheritedAdmin.raw_id_fields)
        self.assertEqual(ma.readonly_fields, BaseAdmin.readonly_fields)