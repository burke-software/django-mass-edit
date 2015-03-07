from django.contrib.auth.models import User
from django.test import TestCase


class SimpleTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username='temporary', password='temporary')

    def test_massadmin_form_generation(self):
        response = self.client.get('/admin/auth/user-masschange/1/')
        self.assertContains(response, 'First name')
