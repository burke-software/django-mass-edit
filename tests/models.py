# coding: utf-8
from django.db import models


class CustomAdminModel(models.Model):
    name = models.CharField(max_length=32)


class InheritedAdminModel(models.Model):
    name = models.CharField(max_length=32)
    fk_field = models.ForeignKey(CustomAdminModel, null=True, blank=True)