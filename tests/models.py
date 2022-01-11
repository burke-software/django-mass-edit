# coding: utf-8
from django.db import models


class CustomAdminModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        app_label = "tests"


class CustomAdminModel2(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        app_label = "tests"


class FieldsetsAdminModel(models.Model):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    class Meta:
        app_label = "tests"



class InheritedAdminModel(models.Model):
    name = models.CharField(max_length=32)
    fk_field = models.ForeignKey(CustomAdminModel, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        app_label = "tests"
