# Generated by Django 3.1.7 on 2021-04-26 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0012_auto_20210421_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='quote_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to='comment.comment'),
        ),
    ]
