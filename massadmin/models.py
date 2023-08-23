from django.db import models


class RightsSupport(models.Model):

    class Meta:

        managed = False

        default_permissions = ()

        permissions = (
            ('can_mass_edit', 'Can perform mass editing'),
        )
