# Generated by Django 3.1.7 on 2021-04-25 05:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20210424_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like_persons',
            field=models.ManyToManyField(related_name='like_articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='value',
            field=models.ImageField(default='avatar.jpg', upload_to='photos/%Y%m%d'),
        ),
    ]
