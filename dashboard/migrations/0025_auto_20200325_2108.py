# Generated by Django 3.0.4 on 2020-03-25 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_auto_20200325_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identifier',
            name='supporting_versions',
            field=models.CharField(blank=True, default='all', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='token_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'KeyWord'), (1, 'Operator'), (2, 'Builtin Functions')], default=0),
        ),
    ]
