# Generated by Django 3.2 on 2021-04-23 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHealthUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeseriesVaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_vaccinations', models.IntegerField(default=0)),
                ('num_fully_vaccinated', models.IntegerField(default=0)),
                ('num_part_vaccinated', models.IntegerField(default=0)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.report')),
            ],
        ),
        migrations.CreateModel(
            name='TimeseriesCasesRegional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_cases', models.IntegerField(default=0)),
                ('total_cases', models.IntegerField(default=0)),
                ('phu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.publichealthunit')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.report')),
            ],
        ),
        migrations.CreateModel(
            name='TimeseriesCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_cases', models.IntegerField(default=0)),
                ('new_deaths', models.IntegerField(default=0)),
                ('new_tests', models.IntegerField(default=0)),
                ('total_cases', models.IntegerField(default=0)),
                ('total_deaths', models.IntegerField(default=0)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.report')),
            ],
        ),
    ]
