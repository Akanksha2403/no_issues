# Generated by Django 4.1.7 on 2023-04-24 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complainapp', '0003_alter_complain_response_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='response_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 25, 7, 24, 52, 919553)),
        ),
    ]
