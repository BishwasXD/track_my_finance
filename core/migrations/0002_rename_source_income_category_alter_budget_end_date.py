# Generated by Django 4.2.2 on 2024-09-04 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='source',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='budget',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 10, 4, 15, 17, 11, 982528, tzinfo=datetime.timezone.utc)),
        ),
    ]
