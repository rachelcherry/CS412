# Generated by Django 5.1.2 on 2024-10-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_article_image_url_alter_article_author"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="image_url",
        ),
        migrations.AddField(
            model_name="article",
            name="image_file",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]