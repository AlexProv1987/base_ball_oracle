# Generated by Django 4.2 on 2023-07-24 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="submitter_message",
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]