# Generated by Django 3.0.4 on 2020-03-22 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200322_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadingquestion',
            name='cource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course'),
        ),
    ]
