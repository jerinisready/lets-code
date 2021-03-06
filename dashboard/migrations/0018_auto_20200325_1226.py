# Generated by Django 3.0.4 on 2020-03-25 06:56

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_user_next_lesson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='solution',
            name='program',
            field=models.TextField(help_text='Write your program here.'),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, null=True)),
                ('question', ckeditor.fields.RichTextField()),
                ('not_useful', models.ManyToManyField(blank=True, related_name='faq_noe_useful', to='dashboard.User')),
                ('related_lessons', models.ManyToManyField(blank=True, to='dashboard.Lesson')),
                ('useful', models.ManyToManyField(blank=True, related_name='faq_useful', to='dashboard.User')),
            ],
        ),
    ]
