# Generated by Django 4.2 on 2023-07-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "questions_api",
            "0002_alter_questions_id_alter_questions_question_reply_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="questions",
            name="question_reply",
            field=models.TextField(max_length=5000),
        ),
    ]
