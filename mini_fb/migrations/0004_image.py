# Generated by Django 5.1.2 on 2024-10-17 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0003_remove_statusmessage_city"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("image_file", models.ImageField(blank=True, upload_to="")),
                ("timestamp", models.DateTimeField(auto_now=True)),
                (
                    "status_message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mini_fb.statusmessage",
                    ),
                ),
            ],
        ),
    ]
