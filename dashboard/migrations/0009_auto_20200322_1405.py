# Generated by Django 3.0.4 on 2020-03-22 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200322_1356'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='cource',
            new_name='course',
        ),
    ]
