# Generated by Django 3.0.4 on 2020-03-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20200322_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='next_task',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
