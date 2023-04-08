# Generated by Django 3.1 on 2022-02-10 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flat", "0004_remove_flat_photos"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="flat_images"),
                ),
                (
                    "flat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="flat.flat"
                    ),
                ),
            ],
        ),
    ]