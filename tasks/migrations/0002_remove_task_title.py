# Generated by Django 5.1.6 on 2025-03-04 13:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="title",
        ),
    ]
