# Generated by Django 3.0.4 on 2020-03-22 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20200322_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Course'),
        ),
        migrations.AlterField(
            model_name='user',
            name='confidence',
            field=models.ManyToManyField(blank=True, to='dashboard.LeadingQuestion'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hint_viewed',
            field=models.ManyToManyField(blank=True, to='dashboard.Question'),
        ),
    ]