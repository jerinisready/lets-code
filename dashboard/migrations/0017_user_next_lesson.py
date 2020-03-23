# Generated by Django 3.0.4 on 2020-03-23 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_remove_user_next_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='next_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Lesson'),
        ),
    ]