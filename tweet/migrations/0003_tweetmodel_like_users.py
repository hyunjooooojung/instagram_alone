# Generated by Django 4.1.1 on 2022-10-27 16:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetmodel',
            name='like_users',
            field=models.ManyToManyField(related_name='like_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
