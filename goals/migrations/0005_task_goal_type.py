# Generated by Django 5.0.2 on 2024-03-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_add_initial_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='goal_type',
            field=models.CharField(choices=[('short_term', '短期'), ('medium_term', '中期'), ('long_term', '長期')], default='', max_length=20),
        ),
    ]
