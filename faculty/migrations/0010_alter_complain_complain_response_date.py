# Generated by Django 4.1.7 on 2023-02-26 18:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0009_complain_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='complain_response_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]