# Generated by Django 5.1.3 on 2024-11-13 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entertainment_recommender", "0004_alter_person_dob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entertainment",
            name="date_added",
            field=models.TextField(),
        ),
    ]
