# Generated by Django 5.0.6 on 2024-07-09 16:24

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
    ]
