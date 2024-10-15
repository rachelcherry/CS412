# Generated by Django 5.1.1 on 2024-10-09 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now=True)),
                ("message", models.TextField()),
                ("city", models.TextField()),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mini_fb.profile",
                    ),
                ),
            ],
        ),
    ]