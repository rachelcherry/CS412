# Generated by Django 5.1.3 on 2024-11-11 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0008_alter_voter_dob_alter_voter_registration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="zip_code",
            field=models.TextField(),
        ),
    ]
