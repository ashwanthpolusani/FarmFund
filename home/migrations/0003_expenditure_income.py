# Generated by Django 5.1.5 on 2025-03-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_crop_delete_addfarm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_id', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_id', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('details', models.TextField()),
            ],
        ),
    ]
