# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0006_partial'),
        ('optimum', '0005_userfacebookpostsanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregatedFacebookDataAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('posts_text', models.TextField(db_column=b'posts_text', default=b'')),
                ('images_text', models.TextField(db_column=b'images_text', default=b'')),
                ('likes_text', models.TextField(db_column=b'likes_text', default=b'')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth')),
            ],
        ),
        migrations.CreateModel(
            name='UserFacebookLikesAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.TextField(db_column=b'like', default=b'')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_django.UserSocialAuth')),
            ],
        ),
    ]