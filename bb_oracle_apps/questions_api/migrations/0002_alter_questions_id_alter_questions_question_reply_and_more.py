# Generated by Django 4.2 on 2023-05-03 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questions",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="questions",
            name="question_reply",
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name="questions",
            name="question_text",
            field=models.TextField(max_length=1024),
        ),
    ]
