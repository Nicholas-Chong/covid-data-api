# Generated by Django 3.2 on 2021-04-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210426_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='test_positivity',
            field=models.FloatField(default=0),
        ),
    ]
