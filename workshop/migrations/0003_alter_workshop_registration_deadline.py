# Generated by Django 5.0.7 on 2024-08-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0002_workshop_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='registration_deadline',
            field=models.DateField(),
        ),
    ]