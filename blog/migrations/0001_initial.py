# Generated by Django 5.0.6 on 2024-07-09 16:15

import django.db.models.deletion
import django.db.models.functions.datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('body', models.TextField()),
                ('slug', models.SlugField(max_length=250)),
                ('publish', models.DateField(db_default=django.db.models.functions.datetime.Now())),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('DB', 'Draft'), ('PB', 'Publish')], default='DB', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish'],
                'indexes': [models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx')],
            },
        ),
    ]
