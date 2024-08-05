# Generated by Django 5.0.7 on 2024-08-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('workshop_title', models.CharField(max_length=500, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('further_info_link', models.URLField(blank=True, null=True)),
                ('prerequisite', models.TextField(blank=True)),
                ('type_of_presence', models.CharField(choices=[('onsite', 'Onsite'), ('hybrid', 'Hybrid'), ('online', 'Online')], max_length=10)),
                ('location', models.CharField(max_length=250)),
                ('host', models.CharField(max_length=300, null=True)),
                ('registration_link', models.URLField(blank=True, null=True)),
                ('max_participants', models.IntegerField()),
                ('tool', models.ManyToManyField(blank=True, to='workshop.tool')),
            ],
        ),
    ]
