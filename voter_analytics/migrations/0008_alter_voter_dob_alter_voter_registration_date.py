# Generated by Django 5.1.2 on 2024-11-07 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0007_alter_voter_precinct_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="dob",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="voter",
            name="registration_date",
            field=models.DateField(),
        ),
    ]
