# Generated by Django 4.1.2 on 2023-02-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_date_eventmodel_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
