# Generated by Django 5.0.2 on 2024-04-14 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
