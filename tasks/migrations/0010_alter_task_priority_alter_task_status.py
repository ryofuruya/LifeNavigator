# Generated by Django 5.0.2 on 2024-04-15 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_task_deadline_alter_task_priority_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('pending', 'Pending')], default='pending', max_length=50),
        ),
    ]
