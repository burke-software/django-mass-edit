# Generated by Django 4.2.5 on 2023-09-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0003_fieldsetsadminmodel_alter_customadminmodel_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StringAdminModel",
            fields=[
                (
                    "primary",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=32)),
            ],
        ),
    ]
