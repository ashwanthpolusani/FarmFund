# Generated by Django 5.1.5 on 2025-03-11 08:44

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_expenditure_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 11, 8, 44, 37, 291112, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
