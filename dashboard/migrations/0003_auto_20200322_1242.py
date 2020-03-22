# Generated by Django 3.0.4 on 2020-03-22 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200322_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='batch',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='day',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='hint',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='logic',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='score',
            name='remarks',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='solution',
            name='suggestions',
            field=models.TextField(blank=True, null=True),
        ),
    ]