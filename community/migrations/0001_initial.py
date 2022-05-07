# Generated by Django 3.1 on 2022-02-03 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
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
                ("object_id", models.PositiveIntegerField()),
                (
                    "rating_star",
                    models.IntegerField(
                        choices=[
                            (1, "One"),
                            (2, "Two"),
                            (3, "Free"),
                            (4, "Four"),
                            (5, "Five"),
                        ]
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
    ]