# Generated by Django 5.1.2 on 2024-11-07 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0002_voter_voter_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="precinct_number",
            field=models.IntegerField(),
        ),
    ]
