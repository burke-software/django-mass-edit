from six.moves.urllib import parse
from django.contrib.auth.models import User
from django.contrib import admin
from django.test import TestCase, override_settings
try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse
from massadmin.massadmin import MassAdmin, get_mass_change_redirect_url

from .admin import CustomAdminForm, BaseAdmin, InheritedAdmin
from .models import CustomAdminModel, InheritedAdminModel


def get_massadmin_url(objects,session):
    if not hasattr(objects, "__iter__"):
        objects = [objects]
    opts = objects[0]._meta
    return get_mass_change_redirect_url(opts,[o.pk for o in objects],session)


def get_changelist_url(model):
    opts = model._meta
    return reverse("admin:{}_{}_changelist".format(
        opts.app_label, opts.model_name))


class AdminViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_massadmin_form_generation(self):
        response = self.client.get(get_massadmin_url(self.user, self.client.session))
        self.assertContains(response, 'First name')

    def test_massadmin_form_generation_with_many_objects(self):
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 2000)]
        response = self.client.get(get_massadmin_url(models, self.client.session))
        self.assertContains(response, 'Change custom admin model')

    @override_settings(MASSEDIT={'SESSION_BASED_URL_THRESHOLD': 3})
    def test_massadmin_form_generation_with_many_objects_settings(self):
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 2)]
        response = self.client.get(get_massadmin_url(models, self.client.session))
        self.assertContains(response, 'Change custom admin model')

    def test_update(self):
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 3)]

        response = self.client.post(get_massadmin_url(models, self.client.session),
                                    {"_mass_change": "name",
                                     "name": "new name"})
        self.assertRedirects(response, get_changelist_url(CustomAdminModel))
        new_names = CustomAdminModel.objects.order_by("pk").values_list("name", flat=True)
        # all models have changed
        self.assertEqual(list(new_names), ["new name"] * 3)

    def test_preserve_filters(self):
        """ Preserve filters which was choosed in lookup form
        """
        model = CustomAdminModel.objects.create(name="aaaa")
        # filter model list by some parameter
        query = "name__startswith=a"
        changelist_url = get_changelist_url(CustomAdminModel) + "?" + query
        # choose mass change action
        response = self.client.post(changelist_url,
                                    {"action": "mass_change_selected",
                                     "_selected_action": model.pk})
        self.assertEqual(response.status_code, 302)
        mass_change_url = response.get("Location")
        # filters add to redirect url
        self.assertEqual(parse.parse_qs(parse.urlparse(mass_change_url).query),
                         {"_changelist_filters": [query]})
        # save mass change form with preserved filters
        response = self.client.post(mass_change_url,
                                    {"_mass_change": "name", "name": "new name"})
        # we are redirected to changelist with filters
        self.assertRedirects(response, changelist_url)

    def test_invalid_form(self):
        """ Save nothing if some forms are invalid
        """
        models = [CustomAdminModel.objects.create(name="model {}".format(i))
                  for i in range(0, 3)]

        response = self.client.post(get_massadmin_url(models, self.client.session),
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
        """ If form is overridden in ModelAdmin, it should be overridden in
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
