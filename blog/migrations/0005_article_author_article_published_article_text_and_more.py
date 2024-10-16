# Generated by Django 5.1.1 on 2024-10-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_remove_article_author_remove_article_image_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.TextField(default="Unknown Author"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="published",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="article",
            name="text",
            field=models.TextField(default="Unknown Author"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="article",
            name="title",
            field=models.TextField(default="Untitled Article"),
            preserve_default=False,
        ),
    ]
